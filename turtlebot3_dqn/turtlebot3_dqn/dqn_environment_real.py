
    #!/usr/bin/env python3
import math
import time
import numpy
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, qos_profile_sensor_data
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from turtlebot3_msgs.srv import Dqn, Goal

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class DQNEnvironmentReal(Node):
    def __init__(self):
        super().__init__('dqn_environment_real')
        print(f"{Colors.HEADER}--- DQN Environment Real (Debug Mode) gestartet ---{Colors.ENDC}")

        self.lidar_group = MutuallyExclusiveCallbackGroup()
        self.client_group = MutuallyExclusiveCallbackGroup()
        self.service_group = ReentrantCallbackGroup()

        self.goal_pose_x = 0.0
        self.goal_pose_y = 0.0
        self.robot_pose_x = 0.0
        self.robot_pose_y = 0.0
        self.robot_pose_theta = 0.0
        
        self.goal_distance = 0.0 
        self.goal_angle = 0.0
        self.goal_received = False 
        self.collision_detected = False
        self.last_scan_time = time.time() 

        self.angular_vel = [1.5, 0.75, 0.0, -0.75, -1.5]
        self.action_names = ["STRONG LEFT", "LEFT", "FORWARD", "RIGHT", "STRONG RIGHT"]
        
        self.state_scan = [3.5] * 24 
        self.min_obstacle_distance = 10.0
        self.target_scan_count = 24 

        qos = QoSProfile(depth=10)
        
        self.cmd_vel_pub = self.create_publisher(TwistStamped, 'cmd_vel', qos)
        self.odom_sub = self.create_subscription(Odometry, 'odom', self.odom_sub_callback, qos)

        self.scan_sub = self.create_subscription(
            LaserScan, 'scan', self.scan_sub_callback, 
            qos_profile_sensor_data, callback_group=self.lidar_group
        )

        self.initialize_env_client = self.create_client(Goal, 'initialize_env', callback_group=self.client_group)
        self.task_succeed_client = self.create_client(Goal, 'task_succeed', callback_group=self.client_group)
        self.task_failed_client = self.create_client(Goal, 'task_failed', callback_group=self.client_group)
        
        self.rl_agent_interface_service = self.create_service(
            Dqn, 'rl_agent_interface', self.rl_agent_interface_callback, callback_group=self.service_group
        )

    def publish_vel(self, lin_x, ang_z):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.twist.linear.x = float(lin_x)
        msg.twist.angular.z = float(ang_z)
        self.cmd_vel_pub.publish(msg)

    def wait_for_future(self, future):
        while not future.done():
            time.sleep(0.01)
        return future.result()

    def euler_from_quaternion(self, quat):
        siny_cosp = 2 * (quat.w * quat.z + quat.x * quat.y)
        cosy_cosp = 1 - 2 * (quat.y * quat.y + quat.z * quat.z)
        return 0, 0, numpy.arctan2(siny_cosp, cosy_cosp)

    def call_initialize_env(self):
        print(f"{Colors.BLUE}[STATE] Wait for the first target...{Colors.ENDC}")
        while not self.initialize_env_client.wait_for_service(timeout_sec=1.0):
            print("... wait for Stage Manager Service ...")
        
        future = self.initialize_env_client.call_async(Goal.Request())
        res = self.wait_for_future(future)
        
        self.goal_pose_x = res.pose_x
        self.goal_pose_y = res.pose_y
        self.goal_received = True
        self.collision_detected = False
        print(f"{Colors.GREEN}[NEW GOAL] Target received: X={self.goal_pose_x:.2f}, Y={self.goal_pose_y:.2f}{Colors.ENDC}")

    def call_task_succeed(self):
        print(f"{Colors.GREEN}[WIN] Target reached!{Colors.ENDC}")
        future = self.task_succeed_client.call_async(Goal.Request())
        res = self.wait_for_future(future)
        self.goal_pose_x = res.pose_x
        self.goal_pose_y = res.pose_y
        self.collision_detected = False
        print(f"{Colors.BLUE}[NEXT GOAL] Go to: X={self.goal_pose_x:.2f}, Y={self.goal_pose_y:.2f}{Colors.ENDC}")

    def call_task_failed(self):
        print(f"{Colors.FAIL}[FAIL] Message to an Stage Manager.{Colors.ENDC}")
        future = self.task_failed_client.call_async(Goal.Request())
        res = self.wait_for_future(future)
        self.goal_pose_x = res.pose_x
        self.goal_pose_y = res.pose_y

    def perform_recovery_maneuver(self):
        print(f"{Colors.WARNING}[RECOVERY] Start: Driving back...{Colors.ENDC}")
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        
        msg.twist.linear.x = -0.15 
        end_time = time.time() + 1.5
        while time.time() < end_time:
            self.cmd_vel_pub.publish(msg)
            time.sleep(0.1)
        
        msg.twist.linear.x = 0.0
        msg.twist.angular.z = 1.0 
        end_time = time.time() + 1.2
        while time.time() < end_time:
            self.cmd_vel_pub.publish(msg)
            time.sleep(0.1)
            
        self.publish_vel(0.0, 0.0)
        print(f"{Colors.GREEN}[RECOVERY] Ready. Agent takes over.{Colors.ENDC}")

    def scan_sub_callback(self, scan):
        self.last_scan_time = time.time()
        
        right_part = scan.ranges[270:]  # Rechts
        left_part = scan.ranges[0:90]   # Vorne + Links
        combined_raw = right_part + left_part 
        
        processed_scan = []
        chunk_size = len(combined_raw) / self.target_scan_count
        
        for i in range(self.target_scan_count):
            start = int(i * chunk_size)
            end = int((i + 1) * chunk_size)
            segment = combined_raw[start:end]
            
            valid_vals = []
            for val in segment:
                if math.isinf(val) or math.isnan(val): 
                    valid_vals.append(3.5)
                elif val < 0.02: 
                    # 0.0 Filterung
                    if self.min_obstacle_distance < 0.25:
                        valid_vals.append(0.0) # Echte Kollision
                    else:
                        valid_vals.append(3.5) # Messfehler
                else:
                    valid_vals.append(val)
            
            val = min(valid_vals) if valid_vals else 3.5
            processed_scan.append(val)

        self.state_scan = processed_scan
        
        all_valid = [r for r in scan.ranges if r > 0.02 and not math.isinf(r)]
        self.min_obstacle_distance = min(all_valid) if all_valid else 10.0

    def odom_sub_callback(self, msg):
        self.robot_pose_x = msg.pose.pose.position.x
        self.robot_pose_y = msg.pose.pose.position.y
        _, _, self.robot_pose_theta = self.euler_from_quaternion(msg.pose.pose.orientation)

    def calculate_state(self):
        dist = math.sqrt((self.goal_pose_x - self.robot_pose_x)**2 + (self.goal_pose_y - self.robot_pose_y)**2)
        path_theta = math.atan2(self.goal_pose_y - self.robot_pose_y, self.goal_pose_x - self.robot_pose_x)
        angle = path_theta - self.robot_pose_theta
        if angle > math.pi: angle -= 2*math.pi
        elif angle < -math.pi: angle += 2*math.pi
        
        self.goal_distance = dist
        self.goal_angle = angle
        
        state = [float(dist), float(angle)] + [float(x) for x in self.state_scan]
        return state

    def rl_agent_interface_callback(self, req, res):
        
        if int(time.time() * 2) % 4 == 0: 
            front_dist = min(self.state_scan[10:14]) 
            act_str = self.action_names[req.action]
            print(f"DIST: {self.goal_distance:.2f}m | ANG: {self.goal_angle:.2f} | LIDAR_FRONT: {front_dist:.2f} | ACTION: {act_str}")

        if req.init:
            if self.collision_detected:
                self.perform_recovery_maneuver()
            self.collision_detected = False
            if not self.goal_received: self.call_initialize_env()

        if (time.time() - self.last_scan_time) > 1.0:
            print(f"{Colors.FAIL}!!! LIDAR TIMEOUT - STOP !!!{Colors.ENDC}")
            self.publish_vel(0.0, 0.0) 
            res.reward = 0.0
            res.done = False
            res.state = self.calculate_state()
            return res
        
        if self.goal_distance < 0.20:
            self.publish_vel(0.0, 0.0)
            self.call_task_succeed() 
            res.reward = 200.0
            res.done = True
            res.state = self.calculate_state()
            return res


        if self.collision_detected:
             self.publish_vel(0.0, 0.0)
             res.reward = 0.0
             res.done = True 
             res.state = self.calculate_state()
             return res

        if self.min_obstacle_distance < 0.20:
            print(f"{Colors.FAIL}!!! CRASH DETECTED ({self.min_obstacle_distance:.2f}m) !!!{Colors.ENDC}")
            self.publish_vel(0.0, 0.0)
            self.call_task_failed() 
            self.collision_detected = True 
            res.reward = -150.0
            res.done = True 
            res.state = self.calculate_state()
            return res

        self.publish_vel(0.15, self.angular_vel[req.action])
        
        res.reward = 1.0 - (2 * abs(self.goal_angle) / math.pi) 
        res.done = False
        res.state = self.calculate_state()
        return res

def main(args=None):
    rclpy.init(args=args)
    node = DQNEnvironmentReal()
    executor = MultiThreadedExecutor() 
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__': 
    main()

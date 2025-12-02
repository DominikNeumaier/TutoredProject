
    
    
#!/usr/bin/env python3
#################################################################################
# Copyright 2019 ROBOTIS CO., LTD.
# Adapted for REAL HARDWARE (Virtual Stage Manager) 
# Optimized for 2m x 2m Arena
#################################################################################

import random
import sys
import math
import rclpy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.qos import QoSProfile
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from turtlebot3_msgs.srv import Goal

class StageManagerReal(Node):

    def __init__(self):
        super().__init__('dqn_stage_real')
   
        self.arena_range = 0.8  
        self.min_goal_distance = 0.5 
        
        self.robot_x = 0.0
        self.robot_y = 0.0

        self.entity_pose_x = 0.5
        self.entity_pose_y = 0.0

        self.callback_group = MutuallyExclusiveCallbackGroup()
        
        self.goal_pub = self.create_publisher(PoseStamped, 'goal_pose', 10)

        qos = QoSProfile(depth=10)
        self.odom_sub = self.create_subscription(
            Odometry, 
            'odom', 
            self.odom_callback, 
            qos
        )


        self.initialize_env_service = self.create_service(
            Goal, 'initialize_env', self.initialize_env_callback, callback_group=self.callback_group)
        self.task_succeed_service = self.create_service(
            Goal, 'task_succeed', self.task_succeed_callback, callback_group=self.callback_group)
        self.task_failed_service = self.create_service(
            Goal, 'task_failed', self.task_failed_callback, callback_group=self.callback_group)
            
        self.get_logger().info("Virtual Stage Manager (2x2m Optimized) started.")
        self.get_logger().info(f"Config: Range={self.arena_range}m, Min Dist={self.min_goal_distance}m")

    def odom_callback(self, msg):
        """current position of the robot"""
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y

    def publish_goal_marker(self):
        """displays target in rviz"""
        msg = PoseStamped()
        msg.header.frame_id = "odom" 
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = self.entity_pose_x
        msg.pose.position.y = self.entity_pose_y
        msg.pose.orientation.w = 1.0 
        self.goal_pub.publish(msg)
        print(f">>> NEW GOAL: X={self.entity_pose_x:.2f}, Y={self.entity_pose_y:.2f}")

    def generate_goal_pose(self):
        valid_goal = False
        attempts = 0
        
        while not valid_goal and attempts < 200:
            attempts += 1
            x = random.uniform(-self.arena_range, self.arena_range)
            y = random.uniform(-self.arena_range, self.arena_range)
            
            dist_to_robot = math.sqrt((x - self.robot_x)**2 + (y - self.robot_y)**2)
            
            dist_to_center = math.sqrt(x**2 + y**2)

            if dist_to_robot > self.min_goal_distance and dist_to_center > 0.1:
                self.entity_pose_x = x
                self.entity_pose_y = y
                valid_goal = True
        
        if not valid_goal:
            print("Warning: No optimal target")
            self.entity_pose_x = random.uniform(-self.arena_range, self.arena_range)
            self.entity_pose_y = random.uniform(-self.arena_range, self.arena_range)


    def initialize_env_callback(self, request, response):
        print("SERVICE: Init request.")
        self.generate_goal_pose()
        self.publish_goal_marker()
        response.pose_x = self.entity_pose_x
        response.pose_y = self.entity_pose_y
        response.success = True
        return response

    def task_succeed_callback(self, request, response):
        print("SERVICE: Success! New Goal.")
        self.generate_goal_pose()
        self.publish_goal_marker()
        response.pose_x = self.entity_pose_x
        response.pose_y = self.entity_pose_y
        response.success = True
        return response

    def task_failed_callback(self, request, response):
        print("SERVICE: Fail (Crash). New Goal.")
        self.generate_goal_pose()
        self.publish_goal_marker()
        response.pose_x = self.entity_pose_x
        response.pose_y = self.entity_pose_y
        response.success = True
        return response

def main(args=None):
    rclpy.init(args=args)
    stage_manager = StageManagerReal()
    
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(stage_manager)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        stage_manager.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

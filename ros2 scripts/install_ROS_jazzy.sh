#!/bin/bash
## jazzy installation via apt for ubuntu Jammy (22.04)
## From official page installation guide :
## https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
## L. Cuvillon

## run with bash ./install_ROS_jazzy.sh
## Note: on TPS machine, there could be some right permission issue on /usr/share/keyring or /etc/ros/ related directories
## Note : expect 3.5Go install for ros-desktop 3.9Go for ros-desktop-full, and +360Mo for gazebo-classics

echo -e "\n###################################"
echo "Ensure that the Ubuntu Universe repository is enabled:"
sudo apt install -y software-properties-common
sudo add-apt-repository -y universe

echo -e "\n###################################"
echo "Add ROS GPG key:"
sudo apt update 
sudo apt install -y curl git
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo -e "\n###################################"
echo "Add ROS repository to source list:"
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

echo -e "\n###################################"
echo "Ensure ubuntu is up-to-date:"
sudo apt update 


read -p "Do you want to proceed with apt upgrade (the packages, not ubuntu version)? (y/n) " yn

case $yn in 
	y ) echo ok, we will proceed
	    sudo apt upgrade -y
	    ;;
	n ) echo no upgrade...;
		exit;;
	* ) echo "invalid response -> will update (ctrl-c if you want to stop)";
	    sleep 10
		exit 1;;
esac

sudo apt upgrade -y

echo -e "\n###################################"
echo "Generates  locale en_UTF8"
sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8

echo -e "\n###################################"
echo "Install full ROS:"
sudo apt install -y ros-jazzy-desktop  # (3Go with gz) or can use ros-jazzy-desktop-full with gazebo (2.6Go)
											 # "desktop" should install -turtlesim, python-3-colcon-extensions, -rosdep
											 #  
sudo apt install -y ros-dev-tools

echo -e "\n###################################"
echo "Install demo, tf2 and urdf demo package"
#From turtlesim demo
sudo apt install -y ros-jazzy-turtlesim ros-jazzy-rqt*
#From tf2 tutorial
sudo apt install -y ros-jazzy-rviz2 ros-jazzy-turtle-tf2-py ros-jazzy-tf2-ros ros-jazzy-tf2-tools ros-jazzy-turtlesim
# Suggested from urdf tutorial
sudo apt install -y ros-jazzy-urdf-tutorial


echo -e "\n###################################"
echo "Install naviguation2 and cartographer"
sudo apt install -y ros-jazzy-navigation2 ros-jazzy-nav2-bringup 		#bringup may not be needed
sudo apt install -y ros-jazzy-cartographer ros-jazzy-cartographer-ros


echo -e "\n###################################"
echo "Install moveit demo requirment"
sudo apt install -y ros-jazzy-moveit    # < ros-jazzy-moveit-planners-ompl ros-jazzy-ompl 
										 # < ros-jazzy-pilz-industrial-motion-planner									 
sudo apt install -y python3-colcon-mixin #for easy parameter passed to colcon (cf movit tutorial)


## For official and ros2_tutorial/manipulation_ros2 from git unistra
sudo apt install -y ros-jazzy-ament-clang-format ros-jazzy-graph-msgs ros-jazzy-rviz-visual-tools \
 ros-jazzy-ros-testing ros-jazzy-gripper-controllers \
 ros-jazzy-control-toolbox ros-jazzy-joint-state-broadcaster ros-jazzy-joint-trajectory-controller \
 ros-jazzy-controller-manager ros-jazzy-ros2-control ros-jazzy-position-controllers freeglut3-dev \
 ros-jazzy-moveit-resources-panda-description ros-jazzy-moveit-resources-panda-moveit-config \
 ros-jazzy-chomp-motion-planner ros-jazzy-moveit-planners-chomp
sudo apt install -y ros-jazzy-moveit-ros-perception ros-jazzy-moveit-hybrid-planning ros-jazzy-moveit-servo \
 ros-jazzy-moveit-visual-tools

# ## For official demo
# sudo apt install -y ros-jazzy-ament-clang-format ros-jazzy-graph-msgs ros-jazzy-rviz-visual-tools \
#  ros-jazzy-ros-testing ros-jazzy-gripper-controllers \
#  ros-jazzy-control-toolbox ros-jazzy-joint-state-broadcaster ros-jazzy-joint-trajectory-controller \
#  ros-jazzy-controller-manager ros-jazzy-ros2-control ros-jazzy-position-controllers freeglut3-dev


# ## For ros2_tutorial/manipulation_ros2 from git unistra
# sudo apt install -y  ros-jazzy-moveit-resources-panda-description ros-jazzy-moveit-resources-panda-moveit-config
# 									# and ros-jazzy-moveit-setup-assistant < installed by moveit package
# sudo apt install -y ros-jazzy-controller-manager 
# sudo apt install -y  ros-jazzy-chomp-motion-planner ros-jazzy-moveit-planners-chomp ros-jazzy-moveit-visual-tools
# 			# and ros-jazzy-moveit-planners-ompl ros-jazzy-ompl ros-jazzy-pilz-industrial-motion-planner < installed by movit package



echo -e "\n###################################"
echo "Install ros Control demo requirment"
sudo apt install -y ros-jazzy-ros2-control ros-jazzy-ros2-controllers

# package for tutorial added by  rosdep install --from-paths ./ -i -y --rosdistro ${ROS_DISTRO} 
sudo apt install -y ros-jazzy-test-msgs liburdfdom-tools \
 ros-jazzy-kinematics-interface-kdl ros-jazzy-ros2-controllers-test-nodes

# for https://github.com/ICube-Robotics/scara_tutorial_ros2 tutorial :
sudo apt install -y ros-jazzy-slider-publisher


echo -e "\n###################################"
echo "Update ROS dependance (ENABLED)"
## will write /etc/ros/rosdep/sources.list.d/20-default.list
sudo rosdep init
rosdep update




#if gazebo-classic wanted, wrt turtlebot3 installation (what we need at least is gazebo and libgazebo11 packages):
# sudo apt install ros-jazzy-gazebo-*
# ignition-gazebo installed by dektop-full, or ros-jazzy-ros-ign 


echo "\n##################################"
echo "install terminator terminal (not a ROS component)"
sudo apt install -y terminator


echo "End of ROS install !!"


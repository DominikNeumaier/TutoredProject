#!/bin/bash
# -i for interactive, neede for source in this script
# Author : Loic Cuvillon 2024

echo -e "\n###################################"
echo "Will update bashrc for ROS_LOCAL classroom"

read -p "Do you want to proceed ? (y/n) " yn

case $yn in 
	y ) echo ok, we will proceed;;
	n ) echo exiting...;
		exit;;
	* ) echo invalid response;
		exit 1;;
esac

## update bashrc for ROS2 CI
echo "export LANG=en_US.UTF-8" >> ~/.bashrc
echo "export LC_ALL=en_US.UTF-8" >> ~/.bashrc
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
echo "export ROS_LOCALHOST_ONLY=1" >> ~/.bashrc

echo -e "\n###################################"
echo " All set. Open a new terminal to take modification into account!"
echo " Note: ROS_LOCALHOST_ONLY is set "

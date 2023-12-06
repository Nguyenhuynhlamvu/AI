#!/usr/bin/env python3
# import rospy
import subprocess

# Initialize the ROS node
# rospy.init_node('external_node')

# Path to your Python node inside the Catkin workspace
catkin_ws_path = '/home/xuanai/catkin_ws'
python_node_path = catkin_ws_path + '/src/library_robot/scripts/goal_broadcaster.py'

# Run the ROS Python node from the Catkin workspace
subprocess.call(['/usr/bin/python3', python_node_path])

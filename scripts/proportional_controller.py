#!/usr/bin/env python3

import rospy

# import our custom message with kp and xd.
from robotics_lab1.msg import Turtlecontrol
# import the Pose message to get the turtle's x coordinate
from turtlesim.msg import Pose
# this is the type of msg the cmd_vel topic expects, we'll use this to set the turtle's velocity.
from geometry_msgs.msg import Twist

# create a global Pose message to store the x value we get from the callback in our subscriber.
pose_msg = Pose()
# create a global Turtlecontrol message to keep track of the kp and xd values we are getting in our subscriber
turtlecontrol_msg = Turtlecontrol()


# save the x value from the pose subscriber
def pose_callback(data):
	global pose_msg
	pose_msg.x = data.x
	# print(pose_msg.x)
	
	
# our subscription to the Turtlecontrol msg will need to use the kp and xd values to calculate
# the appropriate velocity for our turtle friend, save these here for use later
def turtlecontrol_callback(data):
	# save our current kp and xd values
	turtlecontrol_msg.kp = data.kp
	turtlecontrol_msg.xd = data.xd
	#print(f'kp: {data.kp}, xd: {data.xd}')

# function to calculate the velocity of the turtle using current position, desired position, and gain
def calculate_velocity():
	velocity = turtlecontrol_msg.kp * (turtlecontrol_msg.xd - pose_msg.x)
	return velocity


if __name__ == '__main__':
	# initialize the node
	rospy.init_node('proportional_controller', anonymous = True)
	
	# subscribe to the built-in Pose message to get the position info
	rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
	
	# create a new topic control_params and subscribe to it, to get the kp and xd
	rospy.Subscriber('turtle1/control_params', Turtlecontrol, turtlecontrol_callback)
	
	# publish to the velocity_command topic.
	# /turtle1/cmd_vel expects a geometry_msgs/Twist
	velocity = Twist()
	velocity_publisher = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size = 10)
	loop_rate = rospy.Rate(10)
	
	while not rospy.is_shutdown():
		# re-calculate the velocity on each loop
		velocity.linear.x = calculate_velocity()
		# and publish to cmd_vel topic.
		velocity_publisher.publish(velocity)
		loop_rate.sleep()

#!/usr/bin/env python

import rospy, math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

x_real=5
y_real=5
theta_real=0
vel_real=0

#Function to compute the distance module
def EuclidianDistance(x_g,y_g,x_r,y_r):
  return math.sqrt(math.pow((x_g-x_r),2) + math.pow((y_g-y_r),2))

#Function to compute the angular orientation difference thanks to the dot product
def DTheta(x_g,y_g,x_r,y_r,theta,dist):
  if dist>0.5: #Condition to avoid numerical problems
  	return math.acos((math.sin(theta)*(y_g-y_r)+math.cos(theta)*(x_g-x_r))/(dist))
  else:
  	return 0
  	
# Manage the callback

def callback(data):
 #Redeclaration for enabling global variable manipulation
 global x_real
 global y_real
 global theta_real
 global vel_real
 #Code to extract all important values from the message data
 x_real=data.x
 y_real=data.y
 theta_real=data.theta
 vel_real=data.linear_velocity
 #Debugging code to print the message content from console
 #rospy.loginfo("x: "+str(x_real)+" y: "+str(y_real)+" theta: "+str(theta_real))

#
def controller():
  #Node initiation and initiation of variables
  rospy.init_node('Controller', anonymous=True)
  rate = rospy.Rate(60)
  # Manage here the publisher and the subscriber
  rospy.Subscriber('/turtle1/pose', Pose, callback)
  pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
  #
  print("Insert the coordinates that the robot should reach")
  x_goal = input("Insert X: ")
  y_goal = input("Insert y: ")
  
  #Declaration of the structure for imposing the velocities to the turtle
  vel_msg=Twist()
  counter = 0
  
  while not rospy.is_shutdown():
	# Send here the velocity command to the robot
	dist=EuclidianDistance(x_goal,y_goal,x_real,y_real)
  	dtheta=DTheta(x_goal,y_goal,x_real,y_real,theta_real,dist)
	#print("x: "+str(x_real)+" y: "+str(y_real)+" theta: "+str(theta_real))
	
	print("distance error: "+str(dist)+" angular error: " +str(dtheta))
	
	#Behaviour definition, mainly function of the angular difference in order to make the rotation first and then the translation	
	if dtheta>0.01:
		vel_msg.angular.z=20*dtheta
	else: #When correctly directed, I just impose the linear velocity
		vel_msg.angular.z=0
		vel_msg.linear.x=15*dist
		
	#rospy.loginfo(vel_msg)
	#Command to publish the velocity 
	pub.publish(vel_msg)
	counter = counter+1
	#Termination conditions
	if counter >= 900:
	  break
	if EuclidianDistance(x_goal,y_goal,x_real,y_real)<0.1:
	  vel_msg.linear.x=0
	  pub.publish(vel_msg)
	  break
	rate.sleep()
  #Print results
  print("The process has finished in " + str(counter) + " iterations")
  print("The position error is: " + str(EuclidianDistance(x_goal,y_goal,x_real,y_real)))

if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass
if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python

import rospy
import math
import time
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

global x_,y_,heading
x_,y_,heading = 0,0, 0

velocity_msg = Twist()

def deg2rad(th):
    return (th*math.pi/180.0)

def rad2deg(th):
    return (th*180.0/math.pi)

def wrap_pi(th):
    if(th>math.pi):
        return (th - 2*math.pi)
    elif(th<-math.pi):
        return (th + 2*math.pi)
    else:
        return th

def wrap_pi_2(th):
    if(th>math.pi/2.0):
        return (th - math.pi)
    elif(th<-math.pi/2.0):
        return (th + math.pi)
    else:
        return th

def move(velocity_publisher, speed, distance, is_forward):
    global x_, y_
    x0 = x_
    y0 = y_

    distance_travelled = 0.0

    if(is_forward):
        velocity_msg.linear.x = abs(speed)
    else:
        velocity_msg.linear.x = -abs(speed)   
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        distance_travelled = abs(math.sqrt(((x_ - x0)**2) + ((y_ - y0)**2)))
        print(distance_travelled)
        if(distance_travelled<distance):
            velocity_publisher.publish(velocity_msg)
        else:
            break
        rate.sleep()
    velocity_msg.linear.x = 0.0
    velocity_publisher.publish(velocity_msg)         

def rotate(velocity_publisher, angular_velocity, angle, clockwise):
    global heading
    initial_heading = heading
    t0 = time.time()
    angle = deg2rad(angle)
    curr_heading = 0.0

    if(clockwise):
        velocity_msg.angular.z = -abs(angular_velocity)
    else:
        velocity_msg.angular.z = abs(angular_velocity) 

    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        t1 = time.time()
        curr_heading = angular_velocity * (t1 - t0)
        print(rad2deg(curr_heading))
        if(curr_heading<angle):
            velocity_publisher.publish(velocity_msg)
        else:
            break
        rate.sleep()
    velocity_msg.angular.z = 0.0
    velocity_publisher.publish(velocity_msg)   

def go2goal(velocity_publisher, x_g, y_g):
    global x_, y_, heading

    K_linear = 0.2
    K_angular = 2.0
    
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        distance = abs(math.sqrt(((x_g - x_)**2) + ((y_g - y_)**2)))
        angle = math.atan2((y_g - y_), (x_g - x_))
        angle_err = wrap_pi(angle - heading)
        if(math.cos(angle_err)>=0):
            linear_velocity= distance * K_linear
            velocity_msg.linear.x = linear_velocity
            angular_velocity = angle_err * K_angular
            velocity_msg.angular.z = angular_velocity
        else:
            linear_velocity= -distance * K_linear
            velocity_msg.linear.x = linear_velocity
            angular_velocity = wrap_pi_2(angle_err) * K_angular
            velocity_msg.angular.z = angular_velocity        
        print(distance, x_, y_)
        if(distance<0.01):
            velocity_msg.linear.x = 0.0
            velocity_msg.angular.z = 0.0 
        velocity_publisher.publish(velocity_msg)        
        rate.sleep()

def set_desired_orientation(velocity_publisher, ang_vel, des_ang_deg):
    global heading
    diff_angle = des_ang_deg - rad2deg(heading)

    if(diff_angle>=0):
        clockwise = False
    else:
        clockwise = True
    
    rotate(velocity_publisher, ang_vel, abs(diff_angle), clockwise)
    
def spiral_traj(velocity_publisher, vk, wk):
   
    rate = rospy.Rate(1)

    while (wk<=2.0):
        wk = wk + 0.1
        velocity_msg.linear.x = vk
        velocity_msg.linear.y = 0
        velocity_msg.linear.z = 0
        velocity_msg.angular.x = 0
        velocity_msg.angular.y = 0
        velocity_msg.angular.z = wk
        velocity_publisher.publish(velocity_msg)
        rate.sleep()
    velocity_msg.linear.x = 0
    velocity_msg.angular.z = 0
    velocity_publisher.publish(velocity_msg)
   
def posecallback(msg):
    global x_,y_,heading
    x_ = msg.x
    y_ = msg.y
    heading = msg.theta

def main():
    rospy.init_node('turtlesim_move', anonymous= True)
    rospy.Subscriber('/turtle1/pose', Pose, posecallback)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    time.sleep(2)
    # move(velocity_publisher, 0.5, 4.0, True)
    # rotate(velocity_publisher, 0.2, 90.0, False)
    # go2goal(velocity_publisher, 0, 5.544444)
    # set_desired_orientation(velocity_publisher, 0.2, 0)
    spiral_traj(velocity_publisher, 1.0, 0.0)
    # spiral_traj_2(velocity_publisher, 1.0, 2.0)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
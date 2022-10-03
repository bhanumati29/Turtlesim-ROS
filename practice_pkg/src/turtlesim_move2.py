#!/usr/bin/env python

import rospy
import time
import math
import trajectory as traj
import math_utility as m_utl
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

global x_c, y_c, theta_c
x_c, y_c, theta_c = 0.0, 0.0, 0.0

global temp, t_int
temp = True
t_int = 0

velocity_msg = Twist()

def go2goal(xg, yg):
    global x_c, y_c, theta_c
    K_linear = 1.0
    K_angular = 2.0
        
    distance = abs(math.sqrt(((xg - x_c)**2) + ((yg - y_c)**2)))
    print(distance)
    angle = math.atan2((yg - y_c), (xg - x_c))
    angle_err = angle - theta_c
    angle_err = m_utl.wrap_pi(angle_err)
    V = K_linear * distance
    W = K_angular * angle_err
    return V, W

def posecallback(msg):
    global x_c, y_c, theta_c
    x_c = msg.x
    y_c = msg.y
    theta_c = msg.theta

def main():
    rospy.init_node('turtlesim_move', anonymous= True)
    rospy.Subscriber('/turtle1/pose', Pose, posecallback)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    time.sleep(1)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        global t_int
        if (temp == True):
            global temp
            t_int = time.time()
            temp = False
        t = time.time()- t_int
        # xg, yg = traj.Lemiscate_trajectory(t)
        # xg, yg = traj.lemiscate_of_bernoulii(t)
        # xg, yg = traj.circular_trajectory(t)
        # xg, yg = traj.logarithmic_spiral(t)
        # xg, yg = traj.archimedean_spiral(t)
        xg, yg = traj.hippopede_traj(t)
        V, W = go2goal(xg, yg)
        velocity_msg.linear.x = V
        velocity_msg.angular.z = W
        velocity_publisher.publish(velocity_msg)
        rate.sleep()
    velocity_msg.linear.x = 0
    velocity_msg.angular.z = 0
    velocity_publisher.publish(velocity_msg)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
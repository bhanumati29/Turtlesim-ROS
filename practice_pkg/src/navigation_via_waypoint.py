#!/usr/bin/env python

import rospy
import time
import math
import math_utility as m_utl
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

global x_c, y_c, theta_c
x_c, y_c, theta_c = 0.0, 0.0, 0.0

global count
count = 0

velocity_msg = Twist()

def go2goal(xg, yg):
    global x_c, y_c, theta_c
    K_linear = 1.0
    K_angular = 2.0
        
    distance = abs(math.sqrt(((xg - x_c)**2) + ((yg - y_c)**2)))
    angle = math.atan2((yg - y_c), (xg - x_c))
    angle_err = angle - theta_c
    angle_err = m_utl.wrap_pi(angle_err)
    V = 0.5
    W = K_angular * angle_err
    return V, W

def get_des_traj(x_s, y_s, x_goal, y_goal, w_p):
    global x_c, y_c

    x_i = [i[0] for i in w_p]
    y_i = [i[1] for i in w_p]
    x_i.insert(0, x_s)
    y_i.insert(0, y_s)
    x_i.append(x_goal)
    y_i.append(y_goal)
    n = [0]*(len(w_p)+2)
    global count

    while(count<=(len(x_i)-1)):
        xg = x_i[count]
        yg = y_i[count]
        print(xg, yg)
        d = abs(math.sqrt(((x_c - xg)**2) + ((y_c - yg)**2)))
        while not (d<=0.01):
            d = abs(math.sqrt(((x_c - xg)**2) + ((y_c - yg)**2)))
            print(d)
            return xg, yg  
        # n[i] = 1
        count = count + 1
               
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
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        x_s, y_s = 0.5, 0.5
        x_goal, y_goal = 9.0, 9.0
        w_p = [(3.0,3.0), (5.0,2.0), (7.0,6.0), (8.0, 1.0)]
        xg, yg = get_des_traj(x_s, y_s, x_goal, y_goal, w_p)
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
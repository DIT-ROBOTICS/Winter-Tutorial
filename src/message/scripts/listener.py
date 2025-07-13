#!/usr/bin/env python3
#coding:utf-8

import rospy
from std_msgs.msg import Int64

def callbackfunc(msg):
    rospy.loginfo("%d\n",msg.data)

def subscriber():
    rospy.init_node('listener')
    rospy.Subscriber('counter', Int64, callbackfunc)
    rospy.spin()
    
if __name__=='__main__':
    try:
        subscriber()
    except rospy.ROSInterruptException:
        pass

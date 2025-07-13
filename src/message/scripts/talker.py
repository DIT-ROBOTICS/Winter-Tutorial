# !/usr/bin/env python3 
# coding:utf-8
import rospy
from std_msgs.msg import Int64
def publisher():
    rospy.init_node('talker')
    pub = rospy.Publisher('counter', Int64, queue_size = 10)
    count = 0
    while not rospy.is_shutdown():
            pub.publish(count)
            rospy.sleep(1)
            count+=1
    
if __name__=='__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass

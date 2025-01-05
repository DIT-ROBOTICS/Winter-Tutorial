#include "ros/ros.h"
#include "std_msgs/Int64.h"

int main(int argc, char **argv)
{
    ros::init(argc, argv, "talker");
    ros::NodeHandle nh;
    ros::Publisher pub = nh.advertise<std_msgs::Int64>("counter", 10);
    ros::Rate loop_rate(1);
    
    int number = 0;
    std_msgs::Int64 msg;
    
    while(ros::ok())
    {
        msg.data = number;
        // ROS_INFO("%ld", msg.data);
        pub.publish(msg);
        
        number++;
        loop_rate.sleep();
    }
    return 0;
}

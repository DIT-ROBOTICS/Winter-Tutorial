#include "ros/ros.h"
#include "std_msgs/Int64.h"
#include "message/example.h"

void Callback(const message::example::ConstPtr& msg)
{
    printf("(%ld, %s, %d)\n",msg->id,msg->name.c_str(),msg->age);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "listener");
    ros::NodeHandle nh;
    ros::Subscriber sub = nh.subscribe("counter",10,Callback);
    ros::Rate loop_rate(1);
    
    while(ros::ok())
    {
        ros::spinOnce();
        loop_rate.sleep();
    }
    return 0;
}

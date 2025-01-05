#include "ros/ros.h"
#include "std_msgs/Int64.h"

void Callback(const std_msgs::Int64::ConstPtr& msg)
{
    std::cout<<"msg.data = "<<msg->data<<"\n";
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

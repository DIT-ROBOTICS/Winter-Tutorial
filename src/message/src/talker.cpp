#include "ros/ros.h"
#include "std_msgs/Int64.h"
#include "beginner_tutorials/example.h"
#include <queue>

typedef struct student{
    int id;
    std::string name;
    int age;
}st;

int main(int argc, char **argv)
{
    ros::init(argc, argv, "talker");
    ros::NodeHandle nh;
    ros::Publisher pub = nh.advertise<beginner_tutorials::example>("counter", 10);
    ros::Rate loop_rate(1);
    
    beginner_tutorials::example msg;
    std::queue<st> stlist;
    st tmp;
    while(std::cin>>tmp.id>>tmp.name>>tmp.age){
        stlist.push(tmp);
    }
    while(ros::ok() && !stlist.empty())
    {
        msg.age = stlist.front().age;
        msg.name = stlist.front().name;
        msg.id = stlist.front().id;
        stlist.pop();
        // ROS_INFO("%ld", msg.data);
        pub.publish(msg);
        
        loop_rate.sleep();
    }
    return 0;
}

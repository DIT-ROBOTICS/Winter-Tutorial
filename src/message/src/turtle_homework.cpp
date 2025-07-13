#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <turtlesim/Pose.h>


turtlesim::Pose current_pose;

void callback(const turtlesim::Pose::ConstPtr& pose_data)
{
    std::cout<<"current pose = "<<*pose_data<<"\n";
    current_pose = *pose_data;
}

int main(int argc, char **argv)
{
    ros::init(argc,argv,"move_control");
    ros::NodeHandle nh;
    ros::Publisher vel_pub = nh.advertise<geometry_msgs::Twist>("/turtle1/cmd_vel",1);
    ros::Subscriber pose_sub = nh.subscribe("/turtle1/pose",10,callback);
    ros::Rate rate(10);
    geometry_msgs::Twist vel_msg;
    
    ros::Rate loop_rate(10);
    while(ros::ok() && current_pose.x<= 9.5)
    {
        vel_msg.linear.x = 2;
        vel_msg.angular.z = 0.0;
        vel_pub.publish(vel_msg);
        ros::spinOnce();
        loop_rate.sleep();
    }
    while(ros::ok() && current_pose.x<= 10)
    {
        vel_msg.linear.x = 0.1;
        vel_msg.angular.z = 0.0;
        vel_pub.publish(vel_msg);
        ros::spinOnce();
        loop_rate.sleep();
    }
    while(ros::ok() && current_pose.theta>=-1.4)
    {
        vel_msg.linear.x = 0.0;
        vel_msg.angular.z = -0.5;
        vel_pub.publish(vel_msg);
        ros::spinOnce();
        loop_rate.sleep();
    }
    while(ros::ok() && current_pose.theta>=-1.57079)
    {
        vel_msg.linear.x = 0.0;
        vel_msg.angular.z = -0.02;
        vel_pub.publish(vel_msg);
        ros::spinOnce();
        loop_rate.sleep();
    }
    while(ros::ok() && current_pose.y>=0.5)
    {
        vel_msg.linear.x = 2;
        vel_msg.angular.z = 0.0;
        vel_pub.publish(vel_msg);
        ros::spinOnce();
        loop_rate.sleep();
    }
    while(ros::ok() && current_pose.y>0)
    {
        vel_msg.linear.x = 0.1;
        vel_msg.angular.z = 0.0;
        vel_pub.publish(vel_msg);
        ros::spinOnce();
        loop_rate.sleep();
    }
    return 0;
}
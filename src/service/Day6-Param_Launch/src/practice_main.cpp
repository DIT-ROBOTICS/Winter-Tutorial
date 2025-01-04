#include <ros/ros.h>
#include <ros/time.h>
#include <geometry_msgs/Twist.h>
#include <turtlesim/Pose.h>
#include <vector>


/*Global Variable*/
turtlesim::Pose CurrentPose;
turtlesim::Pose TargetPose;
double footprint_x = 0;
double footprint_y = 0;
geometry_msgs::Twist current_vel;
double linear_vel = 0.0;
double angular_vel = 0.0;
double target_theta = 0;
double m = 0;
bool get = 0;
/*Global Variable*/

/*function definition*/
void Callback(const turtlesim::Pose::ConstPtr& pose);
/*function definition*/


int main(int argc, char *argv[])
{
    ros::init(argc, argv, "practice_main");
    ros::NodeHandle nh;
    ros::Publisher turtle_vel_pub = nh.advertise<geometry_msgs::Twist>("/turtle1/cmd_vel", 100);
    ros::Subscriber turtle_pose_sub = nh.subscribe("/turtle1/pose", 100, Callback);
    ros::Rate loop_rate(1);

    if(nh.getParam("/linear_velocity", linear_vel) && nh.getParam("/angular_velocity", angular_vel)){
        
    }else{
        ROS_ERROR("FAIL_TO_GET_PARAM(VEL)");
        return 0;
    }
    

    if(nh.getParam("footprint_x", footprint_x) && nh.getParam("footprint_y", footprint_y)){
        TargetPose.x = footprint_x;
        TargetPose.y = footprint_y;
    }else{
        ROS_ERROR("FAIL_TO_GET_PARAM(FOOTPRINT)");
        return 0;
    }

    

    while (ros::ok())
    {
        current_vel.angular.z = 0;
        if(abs(CurrentPose.x-footprint_x)>=0.15){
            if(CurrentPose.x-footprint_x > 0){
                current_vel.linear.x = -abs(linear_vel);
            }else{
                current_vel.linear.x = abs(linear_vel);
            }
        }else{
            current_vel.linear.x = 0;
        }
        if(abs(CurrentPose.y-footprint_y)>=0.15){
            if(CurrentPose.y-footprint_x > 0){
                current_vel.linear.y = -abs(linear_vel);
            }else{
                current_vel.linear.y = abs(linear_vel);
            }
        }else{
            current_vel.linear.y = 0;
        }

        turtle_vel_pub.publish(current_vel);
        
        ros::spinOnce();
        loop_rate.sleep();
    }
    
    return 0;
}

void Callback(const turtlesim::Pose::ConstPtr& pose){
    CurrentPose.x = pose->x;
    CurrentPose.y = pose->y;
    CurrentPose.theta = pose->theta;
    ROS_ERROR("%f", CurrentPose.x);
    ROS_ERROR("%f", CurrentPose.y);
    ROS_ERROR("%f", CurrentPose.theta);
}
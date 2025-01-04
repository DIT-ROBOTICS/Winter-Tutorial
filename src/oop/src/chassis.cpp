#include "chassis.h"

Chassis::Chassis(float x_0, float y_0, float theta_0, float v_wheels_0[2])
        :x(x_0), y(y_0), theta(theta_0){
            v_wheels[0]=v_wheels_0[0];
            v_wheels[1]=v_wheels_0[1];
        }

void Chassis::forwardKinematics(){
        v_x=(v_wheels[0]+v_wheels[1])*cos(theta)/2;
        v_y=(v_wheels[0]+v_wheels[1])*sin(theta)/2;
        omega=(v_wheels[0]+v_wheels[1])/(radius*2);
    }

void Chassis::poseUpdate(){
        time+=dt;
        x+=v_x*dt;
        y+=v_y*dt;
        theta+=omega*dt;
    }

void Chassis::output(){
        std::cout<<"at "<<time<<"s, ";
        std::cout<<"x: "<<x<<", y: "<<y<<", theta: "<<theta<<std::endl;
    }
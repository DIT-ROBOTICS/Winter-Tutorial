#include <iostream>
#include <math.h>

#ifndef CHASSIS_H
#define CHASSIS_H

class Chassis{
  public:
    Chassis(float x_0, float y_0, float theta_0, float v_wheels_0[2]);
    void forwardKinematics();
    void poseUpdate();
    void output();
    
  private:
    float x;
    float y;
    float theta;
    float v_x=0.0;
    float v_y=0.0;
    float omega=0.0;
    float v_wheels[2]={0.0, 0.0};
    float radius=100;
    float dt=0.01;
    float time=0.0;
};

#endif
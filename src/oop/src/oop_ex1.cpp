#include <iostream>
#include <math.h>

class Chassis{
  public:
    Chassis(float x_0, float y_0, float theta_0, float v_wheels_0[2])
        :x(x_0), y(y_0), theta(theta_0){
            v_wheels[0]=v_wheels_0[0];
            v_wheels[1]=v_wheels_0[1];
        }
    
    void forwardKinematics(){
        v_x=(v_wheels[0]+v_wheels[1])*cos(theta)/2;
        v_y=(v_wheels[0]+v_wheels[1])*sin(theta)/2;
        omega=(v_wheels[0]+v_wheels[1])/(radius*2);
    }
    
    void poseUpdate(){
        time+=dt;
        x+=v_x*dt;
        y+=v_y*dt;
        theta+=omega*dt;
    }
    void output(){
        std::cout<<"at "<<time<<"s, ";
        std::cout<<"x: "<<x<<", y: "<<y<<", theta: "<<theta<<std::endl;
    }
    
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

int main(){
    float time=0.0;
    float wheels[2]={3.0, 3.0};
    Chassis diff(10, 10, 0, wheels);
    for(int i=0;i<5;i++){
        diff.forwardKinematics();
        diff.poseUpdate();
        diff.output();
    }
    return 0;
}

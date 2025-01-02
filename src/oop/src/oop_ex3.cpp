#include <iostream>
#include <math.h>

class Chassis{
  public:
    Chassis(float x_0, float y_0, float theta_0)
        :x(x_0), y(y_0), theta(theta_0){}
    
    virtual void forwardKinematics()=0;
    
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
    
  protected:
    float x;
    float y;
    float theta;
    float v_x=0.0;
    float v_y=0.0;
    float omega=0.0;
    float dt=0.01;
    float time=0.0;
};

class Diff_wheel : public Chassis{
    public:
        Diff_wheel(float x_0, float y_0, float theta_0, float v_wheels_0[2])
          :Chassis(x_0, y_0, theta_0){
                v_wheels[0]=v_wheels_0[0];
                v_wheels[1]=v_wheels_0[1];
                }
        void forwardKinematics() override{
            v_x=(v_wheels[0]+v_wheels[1])*cos(theta)/2;
            v_y=(v_wheels[0]+v_wheels[1])*sin(theta)/2;
            omega=(v_wheels[0]+v_wheels[1])/(radius*2);
            }
    private:
        float v_wheels[2]={0.0, 0.0};
        float radius=100;
};

class Omni_wheel : public Chassis{
    public:
        Omni_wheel(float x_0, float y_0, float theta_0, float v_wheels_0[4])
          :Chassis(x_0, y_0, theta_0){
            for(int i=0;i<4;i++){
                v_wheels[i]=v_wheels_0[i];
            }
          }
        void forwardKinematics() override{
            v_x=0.25*sqrt(2)*(v_wheels[0]-v_wheels[1]-v_wheels[2]+v_wheels[3]);
	        v_y=0.25*sqrt(2)*(v_wheels[0]+v_wheels[1]-v_wheels[2]-v_wheels[3]);
	        omega=(v_wheels[0]+v_wheels[1]+v_wheels[2]+v_wheels[3])/(radius*4.0);
        }
                              
    private:
    float v_wheels[4]={0};
    float radius=200.50;
};

int main(){
    float wheels2[2]={3.0, 3.0};
    float wheels4[4]={3.0, -2.5, -2.7, 3.1};
    Diff_wheel diff(10.0, 10.0, 0.0, wheels2);
    Omni_wheel omni(10.0, 10.0, 0.0, wheels4);
    std::cout<<" -- wheel type: diff wheel -- "<<std::endl;
    for(int i=0;i<5;i++){
        diff.forwardKinematics();
        diff.poseUpdate();
        diff.output();
    }
    std::cout<<" -- wheel type: omni wheel -- "<<std::endl;
    for(int i=0;i<5;i++){
        omni.forwardKinematics();
        omni.poseUpdate();
        omni.output();
    }
    return 0;
}
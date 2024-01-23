// あ　UTF-8
#pragma once

#include <stdio.h>
#include <stdlib.h> //exit()用
#include <math.h>


class Roomba_waypoint
{
public:
    Roomba_waypoint() {}
    Roomba_waypoint(int gain1,int gain2){
        k1 = gain1;
        k2 = gain2;
    }


    void cal_pwm(float now_xpos,float now_ypos,float now_theta,float Target_xpos,float Target_ypos)
    {
        diff_x = Target_xpos-now_xpos;
        diff_y = Target_ypos-now_ypos;
        theta_waypoint = atan2(diff_y,diff_x);
        relative_distance = sqrt((diff_y*diff_y)+(diff_x*diff_x));

        L_pwm = k1*relative_distance + k2*theta_waypoint;
        R_pwm = k1*relative_distance - k2*theta_waypoint;
    }

    float get_diff_distance(){return relative_distance;}
    float get_diff_theta(){return theta_waypoint;}
    int get_Lpwm(){return L_pwm;}
    int get_Rpwm(){return R_pwm;}

private:
int k1;
int k2;
float theta_waypoint = 0;
float relative_distance = 0;
float diff_x = 0;
float diff_y = 0;
int L_pwm = 0;
int R_pwm = 0;
};
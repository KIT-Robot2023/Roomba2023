// あ　UTF-
#pragma once

#include <stdio.h>
#include <stdlib.h> //exit()用
#include <math.h>
#include <time.h>

#ifndef M_PI

#define M_PI 3.14159265358979323846264338327950288

#endif

class Roomba_Odometry
{
public:
    Roomba_Odometry() {}
    Roomba_Odometry(int radius, int tread){
        r = radius/1000.0;
        t = tread/1000.0;
    }

    void get_odometry(int get_now, int get_L_pulse, int get_R_pulse)
    {
        /*calculation odometry*/
        now_time = float(get_now)/1000.0; //ms -> s
        // printf("od.nowtime = %lf\n",now_time);
        printf("%lf,",now_time);
        dt = now_time - pre_time;
        // printf("od.dt = %lf\n",dt);
        L_pulse = float(get_L_pulse);
        R_pulse = float(get_R_pulse);
        // printf("od.L_pulse = %lf,od.R_pulse = %lf\n",L_pulse,R_pulse);

        L_theta = 2 * M_PI *  (L_pulse / 508.8);
        R_theta = 2 * M_PI *  (R_pulse / 508.8);
        // printf("od.L_theta = %lf,od.R_theta = %lf\n",L_theta,R_theta);
        L_omega = (L_theta - L_theta_pre) / dt;
        R_omega = (R_theta - R_theta_pre) / dt;
        // printf("L_theta_diff =%lf,R_theta_diff =%lf\n",L_theta - L_theta_pre,R_theta - R_theta_pre);
        // printf("od.L_omega = %lf,od.R_omega = %lf\n",L_omega,R_omega);
        L_V = r*L_omega;
        R_V = r*R_omega;
        // printf("od.L_V = %lf,od.R_V = %lf\n",L_V,R_V);

        V = 0.5*(L_V+R_V);
        omega = 1/t*(R_V - L_V);
        // printf("od.V = %lf,od.omega = %lf\n",V,omega);

        theta = omega_pre *dt + theta_pre;
        x_pos = V_pre*cos(theta_pre)*dt+x_pos_pre;
        y_pos = V_pre*sin(theta_pre)*dt+y_pos_pre;
        printf("%lf,%lf,%lf\n",theta,x_pos,y_pos);

        /*update val*/
        V_pre = V;
        omega_pre = omega;
        L_theta_pre = L_theta;
        R_theta_pre = R_theta;
        theta_pre = theta;
        x_pos_pre = x_pos;
        y_pos_pre = y_pos;
        pre_time = now_time;
    }

    float get_r(){return r;}
    float get_t(){return t;}

    float get_now_time(){return now_time;}
    float get_dt(){return dt;}

    float get_L_pulse(){return L_pulse;}
    float get_R_pulse(){return R_pulse;}

    float get_L_theta(){return L_theta;}
    float get_R_theta(){return R_theta;}

    float get_L_omega(){return L_omega;}
    float get_R_omega(){return R_omega;}

    float get_L_V(){return L_V;}
    float get_R_V(){return R_V;}

    float get_V(){return V;}
    float get_omega(){return omega;}

    float get_x_pos(){return x_pos;}
    float get_y_pos(){return y_pos;}
    float get_theta(){return theta;}




private:

    float r;
    float t;

    float now_time;
    float pre_time;
    float dt;
    float L_pulse;
    float R_pulse;
    float L_theta;
    float R_theta;
    float L_omega;
    float R_omega;
    float L_V;
    float R_V;
    float V;
    float omega;
    float theta;
    float x_pos;
    float y_pos;

    float V_pre = 0;
    float omega_pre = 0;
    float L_theta_pre = 0;
    float R_theta_pre = 0;
    float theta_pre = 0;
    float x_pos_pre = 0;
    float y_pos_pre = 0;
};
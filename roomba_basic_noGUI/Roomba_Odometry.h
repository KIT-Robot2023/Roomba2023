// あ　UTF-8エンコード
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
        r = radius;
        t = tread;
    }

    void get_odometry(int get_dt, int get_L_pulse, int get_R_pulse)
    {
        /*calculation odometry*/
        dt = float(get_dt);
        L_pulse = float(get_L_pulse);
        R_pulse = float(get_R_pulse);

        L_theta = 2 * M_PI * (L_pulse / 508.8);
        R_theta = 2 * M_PI * (R_pulse / 508.8);

        L_omega = (L_theta - L_theta_pre) / dt;
        R_omega = (R_theta - R_theta_pre) / dt;
        L_V = r*L_omega;
        R_V = r*R_omega;

        V = 0.5*(L_V*R_V);
        omega = 1/t*(R_V - L_V);

        theta = omega_pre *dt + theta_pre;
        x_pos = V_pre*cos(theta_pre)*dt+x_pos_pre;
        y_pos = V_pre*sin(theta_pre)*dt+y_pos_pre;

        /*update val*/
        V_pre = V;
        omega_pre = omega;
        L_theta_pre = L_theta;
        R_theta_pre = R_theta;
        theta_pre = theta;
        x_pos_pre = x_pos;
        y_pos_pre = y_pos;
    }

    float get_x_pos(){return x_pos;}
    float get_y_pos(){return y_pos;}
    float get_theta(){return theta;}
    float get_V(){return V;}
    float get_omega(){return omega;}

private:

    int r;
    int t;

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
﻿// あ　UTF-8エンコード
#include <stdio.h>
#include <stdlib.h> //exit()用
#include <math.h>
#include <time.h>
#include <thread>
#include <Windows.h>
#include <conio.h>
// #include <unistd.h>//usleep用

#include "include/serial.h"
#include "include/roomba_cmd.h"
#include "include/roomba_types.h"
#include "include/Roomba_Odometry.h"

#include "include/init.hpp"
#include "include/sending_command.hpp"
#include "include/time.hpp"
#include "include/timer.hpp"
#include "include/receive.hpp"
#include "include/Sensor.hpp"

#include "include/numkeyCtrl.hpp"

int base_pwm = 50;
int key_input_time = 1;
int ctrl_time = 10;
int update_time = 100;
int i = 0;

int waypoint_mode = 0;
float Target_x[3] = {0.5};
float Target_y[3] = {0.5};

Timer key_input_timer(key_input_time,true);
Timer ctrl_timer(ctrl_time, true);
Timer data_timer(update_time, true);


void mode_change(int port_in)
{
	send_command_one(RB_START, port_in);
	sleep_msec(1000);
	send_command_one(RB_SAFE, port_in);
	sleep_msec(1000);
}

void key_input(void)
{
	int key;
	int port = current_control_port;
	int flag = 1;
	int arg1 = 0;
	int arg2 = 0;

	float now_xpos = 0;
	float now_ypos = 0;
	float now_theta = 0;

	float diff_distance = 0;
	float diff_thata = 0;

	while (flag)
	{
		sleep_msec(100);

		/*オドメトリ関連*/
		if (data_timer())
		{
			get_sensors(port);
			RoombaSensor *rss = &roomba[port].sensor;
			Od.get_odometry(roomba[port].sensor.TimeNow, rss->EncL - ini_Enc_L, rss->EncR - ini_Enc_R);
			now_xpos = Od.get_x_pos();
			now_ypos = Od.get_y_pos();
			now_theta = Od.get_theta();
		}

		// printf("keyf() input: ");
		if (key_input_timer())
		{
			if (_kbhit() && waypoint_mode == 0)
			{
				key = getch();
				switch (key)
				{
				case 'w':
					arg1 = base_pwm;
					arg2 = base_pwm;
					break;
				case 'a':
					arg1 = -base_pwm;
					arg2 = base_pwm;
					break;
				case 's':
					arg1 = -base_pwm;
					arg2 = -base_pwm;
					break;
				case 'd':
					arg1 = base_pwm;
					arg2 = -base_pwm;
					break;
				case 'p':
					waypoint_mode = 1;
					break;
				default:
					arg1 = 0;
					arg2 = 0;
					break;
				}
			}
			else if (waypoint_mode == 0)
			{
					arg1 = 0;
					arg2 = 0;
			}else if(waypoint_mode == 1)
			{
				if(abs(Target_x[i]-now_xpos)> 0.1 || abs(Target_y[i]-now_ypos)> 0.1){
				way.cal_pwm(now_xpos,now_ypos,now_theta,Target_x[i],Target_y[i]);

				arg1 = way.get_Lpwm();
				arg2 = way.get_Rpwm();
				diff_distance = way.get_diff_distance();
				diff_thata = way.get_diff_theta();
				printf("%d,%d,",arg1,arg2);
				printf("%.2f,%.2f\n",diff_distance,diff_thata);
				}else{
					arg1 = 0;
					arg2 = 0;
				}
			}
		}
		if(ctrl_timer()){send_drive_command(arg1, arg2, port);}

		// printf("[%c\n]", key);
		// if (key != '\n')
		// {
		// 	keyf(key, 0, 0);
		// }
		// flag = 0;
	}
}

int main(int argc, char **argv)
{
	int id;

	// シリアルポートスキャン
	comport_scan();

	// シリアルポート初期化
	bool res;
	flag_serial_ready[0] = 0;

	res = rb_serial[0].init(SERIAL_PORT_1, 115200); // 初期化
	rb_serial[0].purge();							// バッファクリア
	if (res != true)
	{
		printf("Port Open Error#0 [%s]\n", SERIAL_PORT_1);
	}
	else
	{
		printf("Port[%s] Ready.\n", SERIAL_PORT_1);
		flag_serial_ready[0] = 1;
	}

	int port = current_control_port;
	init(port); // 変数初期化
	mode_change(port);

	mstime1 = get_millisec(); // 時間計測開始
	printf("mstime1 = %lf\n", mstime1);

	// キーボード割り当て表示
	print_keys();

	get_sensors(port);
	ini_Enc_L = roomba[port].sensor.EncL;
	ini_Enc_R = roomba[port].sensor.EncR;
	RoombaSensor *rss = &roomba[port].sensor;
	Od.get_odometry(roomba[port].sensor.TimeNow, rss->EncL - ini_Enc_L, rss->EncR - ini_Enc_R);

	// キーボード入力受付
	key_input(); // for NoGUI

	return 0;
}
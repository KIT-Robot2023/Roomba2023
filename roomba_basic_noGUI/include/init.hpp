#pragma once

#include "serial.h"
#include "roomba_cmd.h"
#include "roomba_types.h"
#include "Roomba_Odometry.h"
#include "time.hpp"

int ini_Enc_L = 0; // エンコーダーの初期値取得
int ini_Enc_R = 0;

char flag_serial_ready[2];
double mstime2 = 0;
double mstime1 = 0; // msec単位での時間計測

char buf1[1024];
char buf2[1024];
char buf3[1024];
char buf4[1024];
char buf5[1024];

RoombaSystem roomba[2];
serial rb_serial[2]; // シリアル通信クラス

// Odometry Classのインスタンス作成
Roomba_Odometry Od(36, 235);

//--------------
// ☆☆☆☆☆☆☆シリアルポート設定☆☆☆☆☆☆☆☆
// #define SERIAL_PORT_1 "/dev/ttyS16"
#define SERIAL_PORT_1 "\\\\.\\COM11"
//--------------


int current_control_port = 0; // 現在操縦対象のポート
long MotionStartTime = 0; // モーションが始まったときの時刻

void comport_scan()
{
	// COMポートスキャンしてチェック
	serial s1;
	char port_str[128];
	bool res;

	printf("COM port scanning. Available ports: ...\n");
	for (int i = 1; i <= 32; i++)
	{
		sprintf(port_str, "\\\\.\\COM%d", i); // for windows
		// sprintf(port_str,"/dev/ttyS%d",i); //for linux
		res = s1.init(port_str, 115200); // 初期化
		if (res == true)
		{
			printf("[%s]\n", port_str);
			s1.close();
		}
	}
	printf("Done.\n");
}

// char get_sensor_1B(int sensor_no, int port_in)
// int get_sensor_2B(int sensor_no, int port_in)
// char get_sensors(int port_in)
// void print_sensors(int port_in)

// void drive_tires(int dir_in)
// void print_keys(void)



void init(int port_in)
{
	roomba[port_in].odo.theta = 0;
	roomba[port_in].odo.x = 0;
	roomba[port_in].odo.y = 0;
	roomba[port_in].trj_count = 0;
	roomba[port_in].roomba_moving_direction = -1; // 移動方向を表す変数
	roomba[port_in].flag_roomba_moving = 0;		  // 移動中のフラグ
	roomba[port_in].flag_sensor_ready = 0;		  // センサが使えるかどうかのフラグ

	printf("init()..");
	sleep_msec(3000);

	// for(int i=0;i<1000;i++)
	//     usleep(1000);//test
	printf("Done.\n");
}
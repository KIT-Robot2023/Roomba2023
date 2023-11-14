// あ　UTF-8エンコード
#include <stdio.h>
#include <stdlib.h> //exit()用
#include <math.h>
#include <time.h>
#include <thread>
#include <Windows.h>
#include <conio.h>
// #include <unistd.h>//usleep用

#include "serial.h"
#include "roomba_cmd.h"
#include "roomba_types.h"
#include "Roomba_Odometry.h"

#include "init.hpp"
#include "sending_command.hpp"
#include "time.hpp"
#include "timer.hpp"
#include "receive.hpp"
#include "Sensor.hpp"
#include "numkeyCtrl.hpp"

int ctrl_time = 1;
int update_time = 100;

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
	while (flag)
	{
		sleep_msec(100);

		/*オドメトリ関連*/
		if (data_timer())
		{
			get_sensors(port);
			RoombaSensor *rss = &roomba[port].sensor;
			Od.get_odometry(roomba[port].sensor.TimeNow, rss->EncL - ini_Enc_L, rss->EncR - ini_Enc_R);
		}

		printf("keyf() input: ");
		if (ctrl_timer())
		{
			if (_kbhit())
			{
				key = getch();
				switch (key)
				{
				case 'w':
					send_drive_command(200, 200, port);
					break;
				case 'a':
					send_drive_command(-200, 200, port);
					break;
				case 's':
					send_drive_command(-200, -200, port);
					break;
				case 'd':
					send_drive_command(200, -200, port);
					break;
				default:
					break;
				}
			}
			else
			{
				send_drive_command(0, 0, port);
			}
		}

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
	// printf("ini_Enc:");
	// printf("%d,%d",ini_Enc_L,ini_Enc_R);

	// キーボード入力受付
	key_input(); // for NoGUI

	return 0;
}
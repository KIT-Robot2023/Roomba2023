// あ　UTF-8エンコード
#include <stdio.h>
#include "sending_command.hpp"
#include "roomba_types.h"
#include "roomba_cmd.h"
#include "init.hpp"

void drive_tires(int dir_in)
{
	int port = 0;

	RoombaSystem *rb = &roomba[port];

	int speed = 70;
	int speed_rot = 40;
	rb->flag_sensor_ready = 1;

	// if (rb->flag_roomba_moving == 1) // 移動中のボタン入力→移動キャンセル
	// {
	// 	printf("STOP\n");
	// 	rb->CommandSpeedL = 0;
	// 	rb->CommandSpeedR = 0;
	// 	rb->flag_roomba_moving = 0;

	// 	send_drive_command(0, 0, port);

	// 	return;
	// }

	if (dir_in == 1)
	{
		printf("FWD\n");
		rb->CommandSpeedL = speed;
		rb->CommandSpeedR = speed;
		rb->flag_roomba_moving = 1;
	}
	else if (dir_in == 3)
	{
		printf("BACK\n");
		rb->CommandSpeedL = -speed;
		rb->CommandSpeedR = -speed;
		rb->flag_roomba_moving = 1;
	}
	else if (dir_in == 0)
	{
		printf("ROT-CW\n");
		rb->CommandSpeedL = -speed_rot;
		rb->CommandSpeedR = speed_rot;
		rb->flag_roomba_moving = 1;
	}
	else if (dir_in == 2)
	{
		printf("ROT-CCW\n");
		rb->CommandSpeedL = speed_rot;
		rb->CommandSpeedR = -speed_rot;
		rb->flag_roomba_moving = 1;
	}
	else
	{
		printf("STOP\n");
		rb->CommandSpeedL = 0;
		rb->CommandSpeedR = 0;
		rb->flag_roomba_moving = 0;
	}
	send_drive_command(rb->CommandSpeedL, rb->CommandSpeedR, port);
}

void keyf(unsigned char key, int x, int y) // 一般キー入力
{
	// キー入力で指定された処理実行

	//	printf("key[%c],x[%d],y[%d]\n",key,x,y);
	//	printf("key[%c]\n",key);

	int port = current_control_port;
	RoombaSystem *rb = &roomba[port];

	if ((current_control_port == 1) && (flag_serial_ready[1]))
		port = 1;

	switch (key)
	{
	case 'a':
	{
		send_command_one(RB_START, port);

		break;
	}
	case 's':
	{
		send_command_one(RB_STOP, port);
		break;
	}
	case 'd':
	{
		send_command_one(RB_RESET, port);
		// receive_message(port, 256);//初期化メッセージ受信
		receive_initial_message(port); // 初期化メッセージ受信
		break;
	}
	case 'c':
	{
		receive_initial_message(port); // 初期化メッセージ受信　受信バッファクリア
		break;
	}
	case 'f':
	{
		send_command_one(RB_FULL, port);
		break;
	}
	case 'g':
	{
		send_command_one(RB_SAFE, port);
		break;
	}
	case 'z':
	{
		rb->flag_sensor_ready = 1;
		get_sensors(port); // read sensors
		print_sensors(port);
		break;
	}
	case 'x':
	{
		send_song_command(0, port);
		send_play_song_command(0, port);
		break;
	}
	case 'i':
	{
		init(port);
		rb->flag_sensor_ready = 1;
		break;
	}
	case 'v':
	{
		printf("Vacuum ON\n");
		send_pwm_motors_command(0, 100, 100, port); // 吸引ON
		break;
	}
	case 'b':
	{
		printf("Vacuum OFF\n");
		send_pwm_motors_command(0, 0, 0, port); // 吸引OFF
		break;
	}
	case 'w':
	{
		printf("--- Go Back to DOCK! --- \n");
		send_seek_dock_command(port); // ドックに戻る?
		break;
	}
	case '0':
	{
		drive_tires(0);
		break;
	}
	case '1':
	{
		drive_tires(1);
		break;
	}
	case '2':
	{
		drive_tires(2);
		break;
	}
	case '3':
	{
		drive_tires(3);
		break;
	}
	case 'q':
	case 'Q':
	case '\033': /* '\033' は ESC の ASCII コード */
	{
		printf("Exit\n");
		exit(0);
		break;
	}
	case 32: // 32がスペースを表す
	{
		printf("SPACE\n");
		rb->roomba_moving_direction = -1;
		rb->flag_roomba_moving = 0;
		drive_tires(-1); // stop
		break;
	}
	default:
	{
		// print_keys();
		printf("\n");
		break;
	}
	}
}

void print_keys(void)
{
	printf("---------------------\n");
	printf("a: START\n");
	printf("s: STOP\n");
	printf("d: RESET\n");
	printf("g: SAFE\n");
	printf("f: FULL\n");
	printf("c: clear buffer\n");
	printf("\n");
	printf("0: turn right\n");
	printf("1: go forward\n");
	printf("2: turn left\n");
	printf("3: go backward\n");
	printf("\n");
	printf("z: get sensor info\n");
	printf("x: play song\n");
	printf("i: init sensor\n");
	printf("v: vacuum on\n");
	printf("b: vacuum off\n");
	printf("w: dock\n");
	printf("---------------------\n");
}
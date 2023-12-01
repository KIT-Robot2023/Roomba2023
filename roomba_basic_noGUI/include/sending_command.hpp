// あ　UTF-8エンコード
#pragma once

#include <stdio.h>
#include <stdlib.h> //exit()用
#include <math.h>
#include <time.h>
#include <thread>
#include <Windows.h>
#include <conio.h>
#include "init.hpp"

char send_command_one(int cmd_in, int port_in)
{
	// port_inは0 or 1
	char *sbuf = roomba[port_in].sbuf;
	serial *s = &rb_serial[port_in];
	sbuf[0] = (unsigned char)cmd_in; // 1バイト分セット．usigned charに型セット
	s->send(sbuf, 1);				 // コマンド送信

	sprintf(buf1, "send_command_one(%d) rb[%d]sbuf[0]=(%d)\n", cmd_in, port_in, (unsigned char)sbuf[0]);
	printf("%s", buf1);
	return 1;
}

char send_drive_command(int motL, int motR, int port_in)
{
	int byte = 0;
	char *sbuf = roomba[port_in].sbuf;
	serial *s = &rb_serial[port_in];

	sbuf[0] = RB_DRIVE_PWM; // コマンド
	set_drive_command(sbuf + 1, motL, motR);
	byte = 5;
	s->send(sbuf, byte);

	sprintf(buf1, "send_drive_command() rb[%d]sbuf[]=[%d:%d:%d:%d]\n",
			port_in,
			(unsigned char)sbuf[0], (unsigned char)sbuf[1], (unsigned char)sbuf[2], (unsigned char)sbuf[3]);
	// printf(buf1);
	printf("%s", buf1);
	return 1;
}

char send_pwm_motors_command(int main_brush_pwm_in, int side_brush_pwm_in, int vacuum_pwm_in, int port_in)
{
	int byte = 0;
	char *sbuf = roomba[port_in].sbuf;
	serial *s = &rb_serial[port_in];

	sbuf[0] = RB_PWM_MOTORS;	 // コマンド
	sbuf[1] = main_brush_pwm_in; // メインブラシ-127～+127
	sbuf[2] = side_brush_pwm_in; // サイドブラシ-127～+127
	sbuf[3] = vacuum_pwm_in;	 // 吸引 0～+127
	byte = 4;
	s->send(sbuf, byte);

	sprintf(buf1, "send_pwm_motors_command() rb[%d]sbuf[]=[%d:%d:%d:%d]\n",
			port_in,
			(unsigned char)sbuf[0], (unsigned char)sbuf[1], (unsigned char)sbuf[2], (unsigned char)sbuf[3]);
	// printf(buf1);
	printf("%s", buf1);

	return 1;
}

//--------
int send_song_command(int song, int port_in)
{
	// メロディーセットしたもの送信
	// 返り値バイト数
	int byte;
	char *sbuf = roomba[port_in].sbuf;
	serial *s = &rb_serial[port_in];

	byte = set_songA_command(sbuf, song); // songをセット
	s->send(sbuf, byte);				  // コマンド送信

	return byte;
}
//--------
int send_play_song_command(int song, int port_in)
{
	int byte = 2;
	serial *s = &rb_serial[port_in];
	char *sbuf = roomba[port_in].sbuf;

	sbuf[0] = RB_PLAY;
	sbuf[1] = (unsigned char)song; // 1バイト分セット．usigned charに型セット

	s->send(sbuf, byte); // コマンド送信．

	return byte;
}
//--------------------------
int send_seek_dock_command(int port_in)
{
	int byte = 1;
	serial *s = &rb_serial[port_in];
	char *sbuf = roomba[port_in].sbuf;

	sbuf[0] = RB_SEEK_DOCK;
	s->send(sbuf, byte); // コマンド送信．ドック帰還

	return byte;
}
//--------
int send_led_test_command(int port_in)
{
	int byte = 4;
	serial *s = &rb_serial[port_in];
	char *sbuf = roomba[port_in].sbuf;

	sbuf[0] = RB_LEDS;
	sbuf[1] = 0xf;
	sbuf[2] = 0;   // color
	sbuf[3] = 255; // intensity

	s->send(sbuf, byte); // コマンド送信．再生要求

	return byte;
}
//--------------------------
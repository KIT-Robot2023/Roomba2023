// あ　UTF-8エンコード
#include <stdio.h>
#include "serial.h"
#include "roomba_types.h"
#include "sending_command.hpp"
#include "init.hpp"

int receive_message(int port_in, int byte)
{
	// メッセージなど受信
	char *rbuf = roomba[port_in].rbuf;
	serial *s = &rb_serial[port_in];
	// int res=s->receive(rbuf,byte);
	int res = s->receive3(rbuf, byte);
	if (res < 1)
	{
		printf("Error receive_message()\n");
		return 0;
	}
	printf("receive_message(port-%d)\n", port_in);
	printf("---------------\n");
	printf("%s", rbuf);
	printf("\n---------------\n");
	printf("[%d byte]\n", res);
	return 1;
}

int receive_initial_message(int port_in)
{
	// 初期メッセージ受信
	char rbuf[512];
	for (int i = 0; i < 512; i++)
		rbuf[i] = '\0'; // ゼロを詰める
	int res_byte;
	int pos = 0; // バッファ中の位置
	serial *s = &rb_serial[port_in];
	s->purge();
	res_byte = s->receive3(rbuf, 234); // まず234バイト読み込み
	if (res_byte < 1)
	{
		printf("Error receive_message()\n");
		return 0;
	}
	pos = res_byte;
	res_byte = s->receive3(rbuf + pos, 256); // 続きの読み込み（ない場合もあり）
	if (res_byte < 1)
	{
		// printf("Error receive_message()\n");
		// return 0;
		;
	}
	printf("receive_message(port-%d)\n", port_in);
	printf("---------------\n");
	printf("%s", rbuf);
	printf("\n---------------\n");
	printf("[%d byte]\n", pos + res_byte);
	return 1;
}
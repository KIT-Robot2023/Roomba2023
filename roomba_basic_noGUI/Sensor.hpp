#include "sending_command.hpp"
#include "serial.h"
#include "roomba_cmd.h"
#include "roomba_types.h"
#include "time.hpp"
#include "init.hpp"


char get_sensor_1B(int sensor_no, int port_in)
{
	// 1バイトセンサデータ受信
	if (flag_serial_ready[port_in] != 1)
		return -1; ////ポート準備ができていなければ処理しない．

	char *sbuf = roomba[port_in].sbuf;
	char *rbuf = roomba[port_in].rbuf;
	serial *s = &rb_serial[port_in];

	char db = -1; // databyte

	// センサ情報取得
	// 送信要求
	sbuf[0] = RB_SENSORS;				// コマンド
	sbuf[1] = (unsigned char)sensor_no; // センサ番号
	s->send(sbuf, 2);

	// printf("get_sensor_1B(%d) -- ",sensor_no);
	// 受信
	int res = s->receive(rbuf, 1);
	if (res < 1)
	{
		printf("get_sensor_1B:Status");
		printf("%d", res);
		printf("Error get_sensor_1B()\n");
		return 0;
	}

	char b = rbuf[0];
	// printf("[0x%x]=[%d] \n", b,b);

	db = b;
	return db;
}
//--------------------------
int get_sensor_2B(int sensor_no, int port_in)
{
	// 2バイト(int)センサデータ受信
	if (flag_serial_ready[port_in] != 1)
		return -1; ////ポート準備ができていなければ処理しない．

	char *sbuf = roomba[port_in].sbuf;
	char *rbuf = roomba[port_in].rbuf;
	serial *s = &rb_serial[port_in];

	int dat = -1; // databyte
	// センサ情報取得
	// 送信要求
	sbuf[0] = RB_SENSORS;				// コマンド
	sbuf[1] = (unsigned char)sensor_no; // センサ番号
	s->send(sbuf, 2);

	// printf("get_sensor_2B(%d) -- ", sensor_no);
	// 受信
	int res = s->receive(rbuf, 2);
	if (res < 2)
	{
		printf("Error get_sensor_2B()\n");
		return 0;
	}

	int hbyte = rbuf[0];
	int lbyte = rbuf[1];
	// printf("H[0x%x]:L[0x%x]  -- val[%d]\n", hbyte, lbyte, val);

	dat = joint_high_low_byte(hbyte, lbyte);

	return dat;
}
//--------------------------
char get_sensors(int port_in)
{
	if (flag_serial_ready[port_in] != 1)
		return -1; // ポート準備ができていなければ処理しない．

	serial *s = &rb_serial[port_in];
	RoombaSensor *rss = &roomba[port_in].sensor;

	s->purge(); // シリアル通信のバッファクリア

	rss->stat = get_sensor_1B(58, port_in);
	rss->EncL = get_sensor_2B(43, port_in);
	rss->EncR = get_sensor_2B(44, port_in);
	rss->LBumper = get_sensor_1B(45, port_in);
	rss->LBumper_L = get_sensor_2B(46, port_in);
	rss->LBumper_FL = get_sensor_2B(47, port_in);
	rss->LBumper_CL = get_sensor_2B(48, port_in);
	rss->LBumper_CR = get_sensor_2B(49, port_in);
	rss->LBumper_FR = get_sensor_2B(50, port_in);
	rss->LBumper_R = get_sensor_2B(51, port_in);
	// rss->Angle=get_sensor_2B(20,port_in);//値が怪しい
	// rss->Distance=get_sensor_2B(19,port_in);//値が怪しい.ゼロしか出ない

	mstime2 = get_millisec();
	printf("mstime2 = %lf\n", mstime2);
	rss->TimeNow = mstime2 - mstime1; // 現在時刻 201101 clock_gettime()使用
	printf("timenow = %ld\n", rss->TimeNow);

	return 1;
}
//--------------------------
void print_sensors(int port_in)
{
	// RoombaSensor *s1=&sensor1;
	RoombaSensor *rss = &roomba[port_in].sensor;

	if (flag_serial_ready[port_in] != 1)
	{
		// ポート準備ができていない場合
		printf("print_sensors() serial port is not ready.\n");
		return;
	}

	printf("\
    stat=%d,\
    encL=%d,\
    encR=%d,\n\
    LBumper=0x%x,\
    LBumper_L=%d,\
    LBumper_R=%d,\
    Angle=%d,\
    Distance=%d,\
    Time=%.0f,\
    \n",
		   rss->stat,
		   rss->EncL, rss->EncR,
		   rss->LBumper, rss->LBumper_L, rss->LBumper_R,
		   rss->Angle,
		   rss->Distance,
		   rss->TimeNow);

	return;
}
﻿//あ　UTF-8エンコード
#include <stdio.h>
#include <stdlib.h>//exit()用
#include <math.h>
#include <cmath>
#include "serial.h"
#include <time.h>
#include <unistd.h>//usleep用
#include "roomba_cmd.h"
#include "roomba_types.h"
# include <bits/stdc++.h>
#include <iostream>
#include <chrono>
#include <thread>

double mstime1=0;//msec単位での時間計測
double mstime2=0;

//--------------
//☆☆☆☆☆☆☆シリアルポート設定☆☆☆☆☆☆☆☆
//#define SERIAL_PORT_1 "/dev/ttyS16"
#define SERIAL_PORT_1 "\\\\.\\COM4"
//--------------

char buf1[1024];
char buf2[1024];
char buf3[1024];
char buf4[1024];
char buf5[1024];

using std::cout; using std::endl;

//変数2機分用意
RoombaSystem roomba[2];
serial rb_serial[2];//シリアル通信クラス
char flag_serial_ready[2];
int current_control_port=0;//現在操縦対象のポート

long MotionStartTime=0;//モーションが始まったときの時刻

//--------------------------
//時間管理
//--------------------------
double get_millisec(void)
{
	double ms_out;

    #define CPP11_TIME //Linux, WSL, code::blocks64bit版など
    //#undef CPP11_TIME //code::blocks32bit版など

	#ifdef CPP11_TIME
	//Linux C++11用
    struct timespec ts_temp;
	double sec_1,sec_2;
	clock_gettime(CLOCK_REALTIME,&ts_temp);
	sec_1=ts_temp.tv_sec*1000;//秒以上msecに直す
	sec_2=ts_temp.tv_nsec/1000000;//秒以下msecに直す
	ms_out=sec_1+sec_2;
	#else
	//clock()関数を使う方法
	clock_t ck1=clock();
	double sec1=(double)ck1/(CLOCKS_PER_SEC);
	ms_out=sec1*1000;
    #endif

	//printf("get_millisec() %f\n",ms_out);//debug
return ms_out;

}
void sleep_msec(int millisec_in)
{
	//get_millisec()を使う方法．ビジーループで時間を測る
	double sleep_start=get_millisec();
	double now=sleep_start;
	double dt=0;

	while(1)//ビジーループ
	{
		now=get_millisec();//現在時刻
		dt=now-sleep_start;//経過時間
		if(dt>=millisec_in)break;//チェック
	}

	//usleepを使う方法→あまり精度良くない
    //for(int i=0;i<millisec_in;i++)
    //    usleep(1000);//test
}
//--------------------------
//変数初期化
//--------------------------
void init()
{
	for(int i=0;i<2;i++)
	{
    roomba[i].odo.theta=0;
    roomba[i].odo.x=0;
    roomba[i].odo.y=0;
    roomba[i].trj_count=0;
	roomba[i].roomba_moving_direction=-1;//移動方向を表す変数
	roomba[i].flag_roomba_moving=0;//移動中のフラグ
	roomba[i].flag_sensor_ready=0;//センサが使えるかどうかのフラグ
	}

printf("init()..");
	sleep_msec(3000);
//for(int i=0;i<1000;i++)
//    usleep(1000);//test
printf("Done.\n");
}
//--------------------------
//シリアル通信
//--------------------------
void comport_scan()
{
    //COMポートスキャンしてチェック
    serial s1;
    char port_str[128];
    bool res;

    printf("COM port scanning. Available ports: ...\n");
    for(int i=1;i<=32;i++)
    {
        sprintf(port_str,"\\\\.\\COM%d",i); //for windows
        //sprintf(port_str,"/dev/ttyS%d",i); //for linux
        res=s1.init(port_str,115200);//初期化
        if(res==true)
        {
            printf("[%s]\n",port_str);
            s1.close();
        }

    }
    printf("Done.\n");

}

//--------
char send_command_one(int cmd_in, int port_in)
{
//port_inは0 or 1
	char *sbuf=roomba[port_in].sbuf;
	serial *s=&rb_serial[port_in];
	sbuf[0]=(unsigned char)cmd_in;//1バイト分セット．usigned charに型セット
	s->send(sbuf,1);//コマンド送信

	sprintf(buf1, "send_command_one(%d) rb[%d]sbuf[0]=(%d)\n",cmd_in,port_in,(unsigned char)sbuf[0]);
	printf("%s",buf1);
	return 1;
}

//--------
char send_drive_command(int motL, int motR, int port_in)
{
    double sleep_start=get_millisec();
    double now=sleep_start;
    double dt=0;
	int byte=0;
	char *sbuf=roomba[port_in].sbuf;
	serial *s=&rb_serial[port_in];

	sbuf[0]=RB_DRIVE_PWM;//コマンド
	set_drive_command(sbuf+1,motL,motR);
	byte=5;
	s->send(sbuf,byte);

	sprintf(buf1,"send_drive_command() rb[%d]sbuf[]=[%d:%d:%d:%d]\n",
		port_in,
		(unsigned char)sbuf[0],(unsigned char)sbuf[1],(unsigned char)sbuf[2],(unsigned char)sbuf[3]);
		//printf(buf1);
	//printf("%s",buf1);
	return 1;
}
//--------
char send_pwm_motors_command(int main_brush_pwm_in, int side_brush_pwm_in, int vacuum_pwm_in, int port_in)
{
	int byte=0;
	char *sbuf=roomba[port_in].sbuf;
	serial *s=&rb_serial[port_in];

	sbuf[0]=RB_PWM_MOTORS;//コマンド
	sbuf[1]=main_brush_pwm_in;//メインブラシ-127～+127
	sbuf[2]=side_brush_pwm_in;//サイドブラシ-127～+127
	sbuf[3]=vacuum_pwm_in;//吸引 0～+127
	byte=4;
	s->send(sbuf,byte);

	sprintf(buf1,"send_pwm_motors_command() rb[%d]sbuf[]=[%d:%d:%d:%d]\n",
		port_in,
		(unsigned char)sbuf[0],(unsigned char)sbuf[1],(unsigned char)sbuf[2],(unsigned char)sbuf[3]);
		//printf(buf1);
	printf("%s",buf1);

	return 1;
}

//--------
int send_song_command(int song, int port_in)
{
    //メロディーセットしたもの送信
    //返り値バイト数
	int byte;
	char *sbuf=roomba[port_in].sbuf;
	serial *s=&rb_serial[port_in];

	byte=set_songA_command(sbuf, song);//songをセット
	s->send(sbuf,byte);//コマンド送信

	return byte;

}
//--------
int send_play_song_command(int song, int port_in)
{
	int byte=2;
	serial *s=&rb_serial[port_in];
	char *sbuf=roomba[port_in].sbuf;

    sbuf[0]=RB_PLAY;
    sbuf[1]=(unsigned char)song;//1バイト分セット．usigned charに型セット

	s->send(sbuf,byte);//コマンド送信．

	return byte;

}
//--------------------------
int send_seek_dock_command(int port_in)
{
	int byte=1;
	serial *s=&rb_serial[port_in];
	char *sbuf=roomba[port_in].sbuf;

    sbuf[0]=RB_SEEK_DOCK;
	s->send(sbuf,byte);//コマンド送信．ドック帰還

	return byte;

}
//--------
int send_led_test_command(int port_in)
{
	int byte=4;
	serial *s=&rb_serial[port_in];
	char *sbuf=roomba[port_in].sbuf;

    sbuf[0]=RB_LEDS;
    sbuf[1]=0xf;
    sbuf[2]=0;//color
    sbuf[3]=255;//intensity

	s->send(sbuf,byte);//コマンド送信．再生要求

	return byte;

}
//--------------------------
int receive_message(int port_in, int byte)
{
    //メッセージなど受信
    char *rbuf=roomba[port_in].rbuf;
	serial *s=&rb_serial[port_in];
	//int res=s->receive(rbuf,byte);
	int res=s->receive3(rbuf,byte);
	if(res<1)
    {
        printf("Error receive_message()\n");
        return 0;
    }
    printf("receive_message(port-%d)\n",port_in);
    printf("---------------\n");
    printf("%s",rbuf);
    printf("\n---------------\n");
    printf("[%d byte]\n",res);
return 1;
}
//--------------------------
int receive_initial_message(int port_in)
{
    //初期メッセージ受信
    char rbuf[512];
    for(int i=0;i<512;i++)rbuf[i]='\0';//ゼロを詰める
    int res_byte;
    int pos=0;//バッファ中の位置
    serial *s=&rb_serial[port_in];
	s->purge();
	res_byte=s->receive3(rbuf,234);//まず234バイト読み込み
	if(res_byte<1)
    {
        printf("Error receive_message()\n");
        return 0;
    }
    pos=res_byte;
	res_byte=s->receive3(rbuf+pos,256);//続きの読み込み（ない場合もあり）
	if(res_byte<1)
    {
        //printf("Error receive_message()\n");
        //return 0;
        ;
    }
    printf("receive_message(port-%d)\n",port_in);
    printf("---------------\n");
    printf("%s",rbuf);
    printf("\n---------------\n");
    printf("[%d byte]\n",pos+res_byte);
return 1;
}
//--------------------------
char get_sensor_1B(int sensor_no, int port_in)
{
    //1バイトセンサデータ受信
    if(flag_serial_ready[port_in]!=1)return -1;////ポート準備ができていなければ処理しない．

	char *sbuf=roomba[port_in].sbuf;
	char *rbuf=roomba[port_in].rbuf;
	serial *s=&rb_serial[port_in];

	char db=-1;//databyte

	//センサ情報取得
	//送信要求
	sbuf[0]=RB_SENSORS;//コマンド
	sbuf[1]=(unsigned char)sensor_no;//センサ番号
	s->send(sbuf,2);

    //printf("get_sensor_1B(%d) -- ",sensor_no);
	//受信
	int res=s->receive(rbuf,1);
	if(res<1)
    {
        printf("Error get_sensor_1B()\n");
        return 0;
    }

    char b=rbuf[0];
    //printf("[0x%x]=[%d] \n", b,b);

    db=b;
    return db;
}
//--------------------------
int get_sensor_2B(int sensor_no, int port_in)
{
    //2バイト(int)センサデータ受信
    if(flag_serial_ready[port_in]!=1)return -1;////ポート準備ができていなければ処理しない．

	char *sbuf=roomba[port_in].sbuf;
	char *rbuf=roomba[port_in].rbuf;
	serial *s=&rb_serial[port_in];


	int dat=-1;//databyte
	//センサ情報取得
	//送信要求
	sbuf[0]=RB_SENSORS;//コマンド
	sbuf[1]=(unsigned char)sensor_no;//センサ番号
	s->send(sbuf,2);

    //printf("get_sensor_2B(%d) -- ", sensor_no);
	//受信
	int res=s->receive(rbuf,2);
	if(res<2)
    {
        printf("Error get_sensor_2B()\n");
        return 0;
    }

    int hbyte=rbuf[0];
    int lbyte=rbuf[1];
	//printf("H[0x%x]:L[0x%x]  -- val[%d]\n", hbyte, lbyte, val);

	dat=joint_high_low_byte(hbyte,lbyte);

    return dat;
}
//--------------------------
char get_sensors(int port_in)
{
    if(flag_serial_ready[port_in]!=1)return -1;//ポート準備ができていなければ処理しない．

    serial *s=&rb_serial[port_in];
    RoombaSensor *rss=&roomba[port_in].sensor;

	s->purge();//シリアル通信のバッファクリア

rss->stat=get_sensor_1B(58,port_in);
rss->EncL=get_sensor_2B(43,port_in);
rss->EncR=get_sensor_2B(44,port_in);
rss->LBumper=get_sensor_1B(45,port_in);
rss->LBumper_L=get_sensor_2B(46,port_in);
rss->LBumper_FL=get_sensor_2B(47,port_in);
rss->LBumper_CL=get_sensor_2B(48,port_in);
rss->LBumper_CR=get_sensor_2B(49,port_in);
rss->LBumper_FR=get_sensor_2B(50,port_in);
rss->LBumper_R=get_sensor_2B(51,port_in);
rss->Angle=get_sensor_2B(20,port_in);//値が怪しい
rss->Distance=get_sensor_2B(19,port_in);//値が怪しい.ゼロしか出ない

	mstime2=get_millisec();
	rss->TimeNow=mstime2-mstime1;//現在時刻 201101 clock_gettime()使用

return 1;
}
//--------------------------
void print_sensors(int port_in)
{
    //RoombaSensor *s1=&sensor1;
	RoombaSensor *rss=&roomba[port_in].sensor;

    if(flag_serial_ready[port_in]!=1)
    {
        //ポート準備ができていない場合
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
    port_in = %d\n",
       rss->stat,
       rss->EncL,rss->EncR,
       rss->LBumper, rss->LBumper_L,rss->LBumper_R,
        rss->Angle,
        rss->Distance,
        rss->TimeNow,
        port_in
       );

	return;
}
//--------------------------
//-------------------------------------
void drive_tires(int dir_in)
{
	int port = 0;

	RoombaSystem *rb=&roomba[port];

	int speed=70;
	int speed_rot=40;
    rb->flag_sensor_ready=1;

	if(rb->flag_roomba_moving==1)//移動中のボタン入力→移動キャンセル
	{
        printf("STOP\n");
        rb->CommandSpeedL=0;
        rb->CommandSpeedR=0;
        rb->flag_roomba_moving=0;

		send_drive_command(0,0,port);

        return;
	}


    if(dir_in==1)
    {
        printf("FWD\n");
        rb->CommandSpeedL=speed;
        rb->CommandSpeedR=speed;
        rb->flag_roomba_moving=1;
    }
    else if(dir_in==3)
    {
        printf("BACK\n");
        rb->CommandSpeedL=-speed;
        rb->CommandSpeedR=-speed;
        rb->flag_roomba_moving=1;
    }
    else if(dir_in==0)
    {
        printf("ROT-CW\n");
        rb->CommandSpeedL=-speed_rot;
        rb->CommandSpeedR=speed_rot;
        rb->flag_roomba_moving=1;
        printf("aaa\n");
    }
    else if(dir_in==2)
    {
        printf("ROT-CCW\n");
        rb->CommandSpeedL=speed_rot;
        rb->CommandSpeedR=-speed_rot;
        rb->flag_roomba_moving=1;
    }
    else
    {
        printf("STOP\n");
        rb->CommandSpeedL=0;
        rb->CommandSpeedR=0;
        rb->flag_roomba_moving=0;
    }
        send_drive_command(rb->CommandSpeedL,rb->CommandSpeedR,port);

}


//-----------------------
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

//-----------------------
void keyf(unsigned char key , int x , int y)//一般キー入力
{
//キー入力で指定された処理実行

//	printf("key[%c],x[%d],y[%d]\n",key,x,y);
//	printf("key[%c]\n",key);

	int port=current_control_port;
	RoombaSystem *rb=&roomba[port];
	mstime1=get_millisec();//時間計測開始

	if((current_control_port==1)&&(flag_serial_ready[1]))port=1;


    switch(key)
    {
        case 'e':
        {
            break;
        }

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
    		//receive_message(port, 256);//初期化メッセージ受信
    		receive_initial_message(port);//初期化メッセージ受信
    		break;
    	}
    	case 'c':
    	{
    		receive_initial_message(port);//初期化メッセージ受信　受信バッファクリア
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
    	    rb->flag_sensor_ready=1;
    		get_sensors(port);//read sensors
    		print_sensors(port);
    		break;
    	}
    	case 'x':
    	{
    		send_song_command(0,port);
    		send_play_song_command(0,port);
    		break;
    	}
    	case 'i':
    	{
    	    init();
    	    rb->flag_sensor_ready=1;
    	    break;
    	}
    	case 'v':
            {
            printf("Vacuum ON\n");
             send_pwm_motors_command(0,100,100,port);//吸引ON
             break;
            }
    	case 'b':
            {
            printf("Vacuum OFF\n");
             send_pwm_motors_command(0,0,0,port);//吸引OFF
             break;
            }
    	case 'w':
    	{
    	    printf("--- Go Back to DOCK! --- \n");
    		send_seek_dock_command(port);//ドックに戻る?
    		break;
    	}
    	case '0':
    	{
    	    double sleep_start=get_millisec();
            double now=sleep_start;
            double dt=0;
    	    for (int i=0; i<=5;){
                now=get_millisec();//現在時刻
                dt=now-sleep_start;//経過時間
                double dt_1=dt/1000;

                drive_tires(0);
                rb->flag_sensor_ready=1;
                get_sensors(port);//read sensors
                print_sensors(port);
                printf("%lf", dt_1);
                sleep(2);
                i+=1;
                //break;
    		}
    		break;

    	}
    	case '5':
    	{
            double sleep_start=0;
            //double now=sleep_start;
            double now=0;
            double dt=0;//時間用
            double L=0,L1=0,L2=0,Lx=0,Ly=0;
            double L_theta=0, R_theta=0;//シータ角
            double L_theta_1=0, R_theta_1=0;//シータ角
            double thetal=0, thetar=0;
            double L_omega=0, R_omega=0;//ωl,ωr
            double L_v=0, R_v=0;//v
            double w=0,w1=0,w2=0;//ω
            int SL=0,SR=0;
            int S1=0,S2=0,S3=0,S4=0;
            int r=36;//タイヤの半径
            int T=235;//車輪間隔
            double V=0,rad=0;

            sleep(1);
            sleep_start=get_millisec();
            drive_tires(1);
            SR=get_sensor_2B(44, 0);
            SL=get_sensor_2B(43, 0);
            double dt_2=0;

    	    for (int i=0; i<=3;){
                now=get_millisec();//現在時刻
                dt=now-sleep_start;//経過時間
                double dt_1=dt/1000.0;
                rb->flag_sensor_ready=1;
                get_sensors(port);//read sensors
                //Enc
                S1=get_sensor_2B(44, 0);//右
                S2=get_sensor_2B(43, 0);//左
                //S1=i;
                //S2=i;
                S3=S2-SL;
                S4=S1-SR;
                //θ
                L_theta=2*M_PI*S2/508.8;//θ左
                R_theta=2*M_PI*S1/508.8;//θ右
                thetal=L_theta-L_theta_1;
                thetar=R_theta-R_theta_1;
                //ω
                L_omega=thetal/2;//ω左
                R_omega=thetar/2;//ω右
                //v
                L_v=r*L_omega;
                R_v=r*R_omega;
                //V
                V=(L_v+R_v)/2;
                w=(R_v-L_v)/T;
                w2=w-w1;
                rad=w2*dt_1;
                //cout <<std::sin(L_theta);
                //cout <<std::cos(L_theta);
                //距離
                L=w*dt_1;
                Lx=L*sin(rad);
                Ly=L*cos(rad);
                dt_2=dt_1;
                //L1=2*M_PI*36*S3/508.8;//距離左
                //L2=2*M_PI*36*S4/508.8;//距離右
                printf("time:%lf\n", dt_1);
                printf("L:%f\n", L);
                printf("x:%lf,y:%lf,rad:%lf\n",Lx,Ly,rad);
                //printf("EncL:%d,EncR:%d\n", S2,S1);
                //printf("L:%lf, R:%lf\n", thetal,thetar);
                //printf("L_omega:%lf, R_omega:%lf\n", L_omega,R_omega);
                //printf("v_L:%lf, v_R:%lf\n", L_v,R_v);
                //printf("%lf\n",V);
                //print_sensors(port);
                SL=S2;
                SR=S1;
                L_theta_1=2*M_PI*S1/508.8;//θ左
                R_theta_1=2*M_PI*S2/508.8;//θ右
                w1=w;
                i+=1;
                sleep(1);
                //std::this_thread::sleep_for(std::chrono::seconds(1));
                //break;
    		}
    		drive_tires(2);
            break;
    	}
    	case '1':
    	{
    	    drive_tires(1);
            break;
    	}
    	case '2':
    	{
            double sleep_start=get_millisec();
            double now=sleep_start;
            double dt=0;//時間用
            double L=0,L1=0,L2=0;
            double L_theta=0, R_theta=0;//シータ角
            double L_omega=0, R_omega=0;//ω
            double L_v=0, R_v=0;//v
            int SL=0,SR=0;
            int S1=0,S2=0,S3=0,S4=0;
            int r=36;//タイヤの半径

    	    drive_tires(2);
    	    printf("-----------------------");
            SR=get_sensor_2B(44, 0);
            SL=get_sensor_2B(43, 0);
    	    for (int i=0; i<=10;){
                now=get_millisec();//現在時刻
                dt=now-sleep_start;//経過時間
                double dt_1=dt/1000;
                rb->flag_sensor_ready=1;
                get_sensors(port);//read sensors
                //Enc
                S1=get_sensor_2B(44, 0);//右
                S2=get_sensor_2B(43, 0);//左
                S3=S2-SL;
                S4=S1-SR;
                //θ
                L_theta=2*M_PI*S1/508.8;//θ左
                R_theta=2*M_PI*S2/508.8;//θ右
                //ω
                L_omega=L_theta/2;//ω左
                R_omega=R_theta/2;//ω右
                printf("EncL:%d,EncR:%d\n", S2,S1);
                printf("L_theta:%lf, R_theta:%lf\n", L_theta,R_theta);
                printf("L_omega:%lf, R_omega:%lf\n", L_omega,R_omega);
                i+=1;
                //break;
    		}
    		drive_tires(2);
            break;
    	}
    	case '3':
    	{
    	    drive_tires(3);
            break;
    	}
    	case '4'://旋回
    	{
            double sleep_start=0;
            //double now=sleep_start;
            double now=0;
            double dt=0;//時間用
            double L=0,L1=0,L2=0,Lx=0,Ly=0;
            double L_theta=0, R_theta=0;//シータ角
            double L_theta_1=0, R_theta_1=0;//シータ角
            double thetal=0, thetar=0;
            double L_omega=0, R_omega=0;//ωl,ωr
            double L_v=0, R_v=0;//v
            double w=0,w1=0,w2=0;//ω
            int SL=0,SR=0;
            int S1=0,S2=0,S3=0,S4=0;
            int r=36;//タイヤの半径
            int T=235;//車輪間隔
            double V=0,rad=0;

            sleep(1);
            sleep_start=get_millisec();
            drive_tires(1);
            SR=get_sensor_2B(44, 0);
            SL=get_sensor_2B(43, 0);
            double dt_2=0;

    	    for (int i=0; i<=3;){
                now=get_millisec();//現在時刻
                dt=now-sleep_start;//経過時間
                double dt_1=dt/1000.0;
                rb->flag_sensor_ready=1;
                get_sensors(port);//read sensors
                //Enc
                S1=get_sensor_2B(44, 0);//右
                S2=get_sensor_2B(43, 0);//左
                //S1=i;
                //S2=i;
                S3=S2-SL;
                S4=S1-SR;
                //θ
                L_theta=2*M_PI*S2/508.8;//θ左
                R_theta=2*M_PI*S1/508.8;//θ右
                thetal=L_theta-L_theta_1;
                thetar=R_theta-R_theta_1;
                //ω
                L_omega=thetal/2;//ω左
                R_omega=thetar/2;//ω右
                //v
                L_v=r*L_omega;
                R_v=r*R_omega;
                //V
                V=(L_v+R_v)/2;
                w=(R_v-L_v)/T;
                w2=w-w1;
                rad=w2*dt_1;
                printf("time:%lf\n", dt_1);
                printf("rad:%lf\n",rad);
                SL=S2;
                SR=S1;
                L_theta_1=2*M_PI*S1/508.8;//θ左
                R_theta_1=2*M_PI*S2/508.8;//θ右
                w1=w;
                i+=1;
                sleep(1);
                //break;
    		}
    		drive_tires(2);
            break;
    	}
    	case 'q':
    	case 'Q':
    	case '\033':  /* '\033' は ESC の ASCII コード */
        {
            printf("Exit\n");
            exit(0);
            break;
        }
    	case 32: //32がスペースを表す
    	{
    		printf("SPACE\n");
    		rb->roomba_moving_direction=-1;
            rb->flag_roomba_moving=0;
            drive_tires(-1);//stop
    		break;
    	}
        default:
    	{
    		//print_keys();
            printf("\n");
            break;
    	}
    }
}
//-----------------------
void key_input(void)
{
    int key;
    while(1)
    {
    printf("keyf() input: ");
    key=getchar();
    printf("[%c]\n",key);
    keyf(key,0,0);
    }
}

//-----------------------
int main(int argc , char ** argv) {
int id;

	//シリアルポートスキャン
	comport_scan();

	//シリアルポート初期化
  	bool res;
    flag_serial_ready[0]=0;

	res=rb_serial[0].init(SERIAL_PORT_1,115200);//初期化
  	rb_serial[0].purge();//バッファクリア
	if(res!=true)
	  {
	    printf("Port Open Error#0 [%s]\n", SERIAL_PORT_1);
	  }
	  else
      {
          printf("Port[%s] Ready.\n", SERIAL_PORT_1);
          flag_serial_ready[0]=1;
      }


   	init();//変数初期化
	mstime1=get_millisec();//時間計測開始

	//キーボード割り当て表示
	print_keys();

	//キーボード入力受付
    key_input();//for NoGUI


	return 0;
}


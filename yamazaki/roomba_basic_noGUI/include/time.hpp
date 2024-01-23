#pragma once

// あ　UTF-8エンコード
#include <math.h>
#include <time.h>

//--------------------------
// 時間管理
//--------------------------
double get_millisec(void)
{
	double ms_out;

// #define CPP11_TIME //Linux, WSL, code::blocks64bit版など
#undef CPP11_TIME // code::blocks32bit版など

#ifdef CPP11_TIME
	// Linux C++11用
	struct timespec ts_temp;
	double sec_1, sec_2;
	clock_gettime(CLOCK_REALTIME, &ts_temp);
	sec_1 = ts_temp.tv_sec * 1000;	   // 秒以上msecに直す
	sec_2 = ts_temp.tv_nsec / 1000000; // 秒以下msecに直す
	ms_out = sec_1 + sec_2;
#else
	// clock()関数を使う方法
	clock_t ck1 = clock();
	double sec1 = (double)ck1 / (CLOCKS_PER_SEC);
	ms_out = sec1 * 1000;
#endif

	// printf("get_millisec() %f\n",ms_out);//debug
	return ms_out;
}

void sleep_msec(int millisec_in)
{
	// get_millisec()を使う方法．ビジーループで時間を測る
	double sleep_start = get_millisec();
	double now = sleep_start;
	double dt = 0;

	while (1) // ビジーループ
	{
		now = get_millisec();	// 現在時刻
		dt = now - sleep_start; // 経過時間
		if (dt >= millisec_in)
			break; // チェック
	}

	// usleepを使う方法→あまり精度良くない
	// for(int i=0;i<millisec_in;i++)
	//     usleep(1000);//test
}
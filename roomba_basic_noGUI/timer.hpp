#pragma once
#include "time.hpp"

class Timer
{
public:
    Timer() {}

    Timer(int time_ms, bool auto_reload = false) { timer_set(time_ms, auto_reload); }

    void timer_set(int time, bool auto_reload = false)
    {
        start_time = get_millisec();
        set_time = time;
    }

    bool check()
    {
    }

private:
    int set_time;
    int start_time;
    bool reset;
};

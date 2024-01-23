#pragma once
#include "time.hpp"

class Timer
{
public:
    Timer() {}
    Timer(int time_ms, bool auto_reload = false) { timer_set(time_ms, auto_reload); }

    void timer_set(int time_ms, bool auto_reload_ = false)
    {
        start_time = get_millisec();
        set_time = time_ms;
        auto_reload = auto_reload_;
    }
    bool check(){
        bool is_over = get_millisec() - start_time >= set_time;
        if(is_over && auto_reload) start_time = get_millisec();
        return is_over;
    }
    void operator()(int time_ms, bool auto_reload){timer_set(time_ms,auto_reload);}
    bool operator()(){return check();}

private:
    int set_time = 0;
    int start_time = 0;
    bool auto_reload = 0;
};

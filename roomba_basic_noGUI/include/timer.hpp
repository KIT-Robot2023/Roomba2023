#pragma once
#include <chrono>

class Timer {
public:
    Timer(){};
    int setup() { return 0; }

    void set(std::chrono::milliseconds time, bool auto_reset = false) {
        settedTime = time;
        startTime = std::chrono::steady_clock::now();
        this->auto_reset = auto_reset;
    };
    bool check() {
        if (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - startTime)
                .count() >= settedTime.count()) {
            if (auto_reset) startTime = std::chrono::steady_clock::now();
            return true;
        }
        return false;
    }
    void operator()(std::chrono::milliseconds time, bool auto_reset = false) {
        set(time);
        this->auto_reset = auto_reset;
    }
    bool operator()() { return check(); }

private:
    std::chrono::milliseconds settedTime;
    std::chrono::steady_clock::time_point startTime = std::chrono::steady_clock::now();
    bool auto_reset = false;
};

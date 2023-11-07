#pragma once
#include <chrono>
#include <iostream>

#include "diff2_odometry.hpp"
#include "roomba_command.hpp"

namespace roomba {

struct Sensors {
    char stat;
    int open_interfase_Mode;
    int enc_left;
    int enc_right;
    char LBumper;
    int LBumper_L;
    int LBumper_FL;
    int LBumper_CL;
    int LBumper_CR;
    int LBumper_FR;
    int LBumper_R;
    int Angle;
    int Distance;
    long TimeNow;   // 現在時刻
    long TimePrev;  // 前回計測した時刻
    int EncL_Prev;  // 前回エンコーダ値
    int EncR_Prev;  // 前回エンコーダ値
};
class Roomba {
public:
    Roomba() = default;
    ~Roomba() = default;
    Roomba(roomba::Command &command, diff2_odometry::Diff2Odometry &odometry)
        : command_(command), odometry_(odometry){};
    bool init();
    void cycle();
    void drive(int left_vel, int right_vel);  //[mm/s]
    const Sensors &sensors() { return sensors_; };
    const diff2_odometry::Diff2OdometryState &odo() { return odometry_.state(); }
    void set_mode();
    std::chrono::steady_clock::time_point current_time() const { return current_time_; };

private:
    void get_sensors_() {
        sensors_.enc_left = command_.get_encoder_left();
        sensors_.enc_right = command_.get_encoder_right();
    };
    roomba::Command &command_;
    diff2_odometry::Diff2Odometry &odometry_;
    roomba::Sensors sensors_;

    std::chrono::steady_clock::time_point prev_time_;
    std::chrono::steady_clock::time_point current_time_;
};
}  // namespace roomba
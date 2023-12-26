#pragma once
#include <chrono>
#include <iostream>

#include "pure_pursuit.hpp"
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
    long TimeNow;  // 現在時刻
};
class Roomba {
public:
    Roomba() = default;
    ~Roomba() = default;
    Roomba(roomba::Command &command, diff2_odometry::Diff2Odometry &odometry, pure_pursuit::PurePursuit &pure_pursuit)
        : command_(command), odometry_(odometry), pure_pursuit_(pure_pursuit){};
    enum class SystemMode {
        init = 0,
        manual,
        path_tracking,
    } system_mode = SystemMode::manual;

    bool init();
    void cycle();
    void drive(double left_vel, double right_vel);  //[m/s]
    void drive(pure_pursuit::Output output) { drive(output.left, output.right); };
    void set_path(pure_pursuit::Path path) { pure_pursuit_.set_path(path); };
    void start_path_tracking() {
        system_mode = SystemMode::path_tracking;
        pure_pursuit_.start_tracking();
    }
    const Sensors &sensors() { return sensors_; };
    const diff2_odometry::Diff2OdometryState &odo() { return odometry_.state(); }
    void set_mode(const uint8_t cmd) { command_.send_one_command(cmd); };
    std::chrono::steady_clock::time_point current_time() const { return current_time_; };

private:
    roomba::Command &command_;
    diff2_odometry::Diff2Odometry &odometry_;
    pure_pursuit::PurePursuit &pure_pursuit_;
    roomba::Sensors sensors_;

    std::chrono::steady_clock::time_point prev_time_;
    std::chrono::steady_clock::time_point current_time_;
};
}  // namespace roomba
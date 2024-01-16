#include "../include/roomba.hpp"

#include <chrono>
#include <iostream>
#include <thread>

using namespace roomba;

bool Roomba::init() {
    if (command_.init()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        std::cout << "init success. send start command." << std::endl;
        command_.send_start_command();
    } else {
        std::cout << "init error." << std::endl;
    }
}

void Roomba::cycle() {
    current_time_ = std::chrono::steady_clock::now();
    auto dt_ms = std::chrono::duration_cast<std::chrono::milliseconds>(current_time_ - prev_time_);
    const double dt = dt_ms.count() / 1000.0;
    odometry_.cycle();

    if (system_mode == SystemMode::path_tracking) {
        pure_pursuit_.calculate(odometry_.pose());
        drive(pure_pursuit_.output());
    }

    prev_time_ = current_time_;
}

void Roomba::drive(double left_vel, double right_vel) {
    // if (system_mode == SystemMode::manual) {
    std::cout << "in drive()\n left[m/s]:  " << left_vel << " right[m/2]: " << right_vel
              << " left[mm/s]:" << (int)(left_vel * 1000) << " right[mm/s]: " << (int)(right_vel * 1000) << std::endl;
    command_.send_drive_direct_command((int)(left_vel * 1000), (int)(right_vel * 1000));
    // }
}

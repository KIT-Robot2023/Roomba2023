#include "../include/roomba.hpp"

#include <chrono>
#include <iostream>
#include <thread>

using namespace roomba;

bool Roomba::init() {
    if (command_.init()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        command_.send_start_command();
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        command_.send_safe_mode_command();
    } else {
        std::cout << "init error." << std::endl;
    }
}

void Roomba::cycle() {
    current_time_ = std::chrono::steady_clock::now();
    auto dt_ms = std::chrono::duration_cast<std::chrono::milliseconds>(current_time_ - prev_time_);
    const double dt = dt_ms.count() / 1000.0;

    odometry_.cycle();

    // get_sensors_();

    prev_time_ = current_time_;
}

void Roomba::drive(int left_vel, int right_vel) { command_.send_drive_direct_command(left_vel, right_vel); }


bool VertialRoomba::init() { return true; }

void VertialRoomba::cycle() {
    current_time_ = std::chrono::steady_clock::now();
    auto dt_ms = std::chrono::duration_cast<std::chrono::milliseconds>(current_time_ - prev_time_);
    const double dt = dt_ms.count() / 1000.0;

    odometry_.cycle();

    // get_sensors_();

    prev_time_ = current_time_;
}

void VertialRoomba::drive(int left_vel, int right_vel) { return; }

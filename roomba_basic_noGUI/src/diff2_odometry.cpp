#include "../include/diff2_odometry.hpp"

#include <cmath>
#include <iostream>

namespace diff2_odometry {
void Diff2Odometry::cycle() {
    const auto current_time_ = std::chrono::steady_clock::now();
    auto dt_ms = std::chrono::duration_cast<std::chrono::milliseconds>(current_time_ - prev_time_);
    const double dt = dt_ms.count() / 1000.0;

    const int left_count = command_.get_encoder_left();
    const int right_count = command_.get_encoder_right();

    const double left_omega = count_to_rad_((left_count - prev_left_count_) / dt);
    const double right_omega = count_to_rad_((right_count - prev_right_count_) / dt);

    const double left_vel = omega_to_vel_(left_omega);
    const double right_vel = omega_to_vel_(right_omega);

    const double v = (left_vel + right_vel) / 2.0;
    const double w = (right_vel - left_vel) / config_.wheel_tread;

    state_.x = prev_state_.x + prev_state_.v * cos(prev_state_.theta) * dt;
    state_.y = prev_state_.y + prev_state_.v * sin(prev_state_.theta) * dt;
    state_.theta = prev_state_.theta + w * dt;
    state_.v = v;
    state_.w = w;

    std::cout << " left_cout: " << left_count << " right_count: " << right_count << " left_omega: " << left_omega
              << " right_omega: " << right_omega << " left_vel: " << left_vel << " right_vel: " << right_vel
              << " vel: " << state_.v << " W: " << state_.w << std::endl;

    prev_left_count_ = left_count;
    prev_right_count_ = right_count;
    prev_state_ = state_;
    prev_time_ = current_time_;
};
}  // namespace diff2_odometry
#include "../include/diff2_odometry.hpp"

#include <cmath>
#include <iostream>
using util::sign;

namespace diff2_odometry {
void Diff2Odometry::cycle() {
    const auto current_time_ = std::chrono::steady_clock::now();
    auto dt_ms = std::chrono::duration_cast<std::chrono::milliseconds>(current_time_ - prev_time_);
    const double dt = dt_ms.count() / 1000.0;

    const int left_count = command_.get_encoder_left();
    const int right_count = command_.get_encoder_right();

    if (init_flag_) {
        current_left_count_ = left_count;
        current_right_count_ = right_count;
        init_flag_ = false;
    } else {
        auto &pose = state_.pose;
        auto &twist = state_.twist;
        const int dt_left_count = delta_count_(left_count - prev_left_count_);
        const int dt_right_count = delta_count_(right_count - prev_right_count_);

        current_left_count_ = prev_left_count_ + dt_left_count;
        current_right_count_ = prev_right_count_ + dt_right_count;

        const double left_omega = count_to_rad_((dt_left_count) / dt);
        const double right_omega = count_to_rad_((dt_right_count) / dt);

        const double left_vel = omega_to_vel_(left_omega);
        const double right_vel = omega_to_vel_(right_omega);

        const double v = (left_vel + right_vel) / 2.0;
        const double w = (right_vel - left_vel) / config_.wheel_tread;

        pose.point.x = pose.point.x + twist.v * cos(pose.theta) * dt;
        pose.point.y = pose.point.y + twist.v * sin(pose.theta) * dt;
        pose.theta = pose.theta + w * dt;
        twist.v = v;
        twist.w = w;
    }

    prev_left_count_ = current_left_count_;
    prev_right_count_ = current_right_count_;
    prev_state_ = state_;
    prev_time_ = current_time_;
};
}  // namespace diff2_odometry
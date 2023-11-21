#pragma once
#include <chrono>

#include "roomba_command.hpp"
#include "util.hpp"

namespace diff2_odometry {
struct Diff2OdometryConfig {
    Diff2OdometryConfig(const int encoder_count_per_revolution, const int encoder_count_range,
                        const double wheel_radius, const double wheel_tread)
        : encoder_count_per_revolution(encoder_count_per_revolution),
          encoder_count_range(encoder_count_range),
          wheel_radius(wheel_radius),
          wheel_tread(wheel_tread){};
    const int encoder_count_per_revolution;
    const int encoder_count_range;
    const double wheel_radius;
    const double wheel_tread;
};

struct Diff2OdometryState {
    double x = 0;
    double y = 0;
    double theta = 0;
    double v = 0;
    double w = 0;
};

class Diff2Odometry {
public:
    Diff2Odometry(roomba::Command &command, Diff2OdometryConfig &config) : command_(command), config_(config) {
        prev_left_count_ = 0;
        prev_right_count_ = 0;
    };
    void cycle();
    const Diff2OdometryState &state() const { return state_; };
    double x() { return state_.x; };
    double y() { return state_.y; };
    double theta() { return state_.theta; }
    double v() { return state_.v; };
    double w() { return state_.w; };

private:
    roomba::Command &command_;
    const Diff2OdometryConfig &config_;

    std::chrono::steady_clock::time_point prev_time_;
    Diff2OdometryState prev_state_;
    Diff2OdometryState state_;
    int prev_left_count_;
    int prev_right_count_;

    double count_to_rad_(const double count) {
        return 2.0 * util::pi_d * count / config_.encoder_count_per_revolution;
    };
    double omega_to_vel_(const double omega) { return omega * config_.wheel_radius; };
    int delta_count_(int dt_count) {
        if (abs(dt_count) >= config_.encoder_count_range / 2) {
            return util::sign(dt_count) * config_.encoder_count_range - dt_count;
        } else {
            return dt_count;
        }
    };
};
}  // namespace diff2_odometry
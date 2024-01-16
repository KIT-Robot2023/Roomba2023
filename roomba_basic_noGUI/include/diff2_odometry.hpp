#pragma once
#include <chrono>
#include <vector>

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
struct Point {
    Point(double x, double y) : x(x), y(y){};
    double x;
    double y;
};
struct Pose {
    Point point = Point(0.0, 0.0);
    double theta = 0.0;
};
struct Twist {
    double v = 0.0;
    double w = 0.0;
};
struct Diff2OdometryState {
    Pose pose;
    Twist twist;
};

class Diff2Odometry {
public:
    Diff2Odometry(roomba::Command &command, Diff2OdometryConfig &config)
        : command_(command), config_(config), init_flag_(true) {
        prev_left_count_ = 0;
        prev_right_count_ = 0;
    };
    void cycle();
    const Diff2OdometryState &state() const { return state_; }
    const Pose &pose() const { return state_.pose; }
    const Twist &twist() const { return state_.twist; }
    double x() { return pose().point.x; }
    double y() { return pose().point.y; }
    double theta() { return pose().theta; }
    double v() { return twist().v; }
    double w() { return twist().w; }
    int encoder_left() { return current_left_count_; }
    int encoder_right() { return current_right_count_; }

private:
    roomba::Command &command_;
    const Diff2OdometryConfig &config_;

    bool init_flag_;
    std::chrono::steady_clock::time_point prev_time_;
    Diff2OdometryState prev_state_;
    Diff2OdometryState state_;
    int current_left_count_;
    int current_right_count_;
    int prev_left_count_;
    int prev_right_count_;

    double count_to_rad_(const double count) {
        return count * (2.0 * util::pi_d / config_.encoder_count_per_revolution);
    }
    double omega_to_vel_(const double omega) { return omega * config_.wheel_radius; }
    int delta_count_(int dt_count) {
        if (abs(dt_count) >= config_.encoder_count_range / 2) {
            return util::sign(dt_count) * config_.encoder_count_range - dt_count;
        } else {
            return dt_count;
        }
    }
};
}  // namespace diff2_odometry
#pragma once

#include <vector>

#include "../include/diff2_odometry.hpp"

namespace pure_pursuit {
struct Output {
    double left;
    double right;
};
struct Path {
    std::vector<diff2_odometry::Point> points;
};
struct PurePursuitConfig {
    PurePursuitConfig() = default;
    ~PurePursuitConfig() = default;
    PurePursuitConfig(double vel_gain, double omega_gain, double vel_limit, double lookahead_length, double tolerance)
        : vel_gain(vel_gain),
          omega_gain(omega_gain),
          vel_limit(vel_limit),
          lookahead_length(lookahead_length),
          tolerance(tolerance) {}
    double vel_gain;
    double omega_gain;
    double vel_limit;
    double lookahead_length;
    double tolerance;
};
class PurePursuit {
public:
    PurePursuit() = default;
    ~PurePursuit() = default;
    PurePursuit(PurePursuitConfig config) : config_(config), setted_flag_(false), tracking_flag_(false){};

    void set_path(Path path);
    void start_tracking();
    void stop_tracking() { tracking_flag_ = false; };
    void calculate(diff2_odometry::Pose current_pose);
    bool tracking() const { return tracking_flag_; }
    Output output() const { return output_; };

private:
    PurePursuitConfig config_;
    Path path_;
    bool setted_flag_ = false;
    bool tracking_flag_ = false;
    Output output_;
    int path_count_;

    bool point_is_equal(diff2_odometry::Point num1, diff2_odometry::Point num2) {
        if ((num1.x == num2.x) && (num1.y == num2.y)) { return true; }
        return false;
    }
};
}  // namespace pure_pursuit
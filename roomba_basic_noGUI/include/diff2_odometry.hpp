#include <chrono>

#include "roomba_command.hpp"
#include "util.hpp"

namespace diff2_odometry {
struct Diff2OdometryConfig {
    Diff2OdometryConfig(const int encoder_count_per_revolution, const double wheel_radius, const double wheel_tread)
        : encoder_count_per_revolution(encoder_count_per_revolution),
          wheel_radius(wheel_radius),
          wheel_tread(wheel_tread){};
    const int encoder_count_per_revolution;
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
    const Diff2OdometryState &state() { return state_; };

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
};
}  // namespace diff2_odometry
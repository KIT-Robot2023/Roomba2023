#include "../include/pure_pursuit.hpp"

#include <cmath>
#include <iostream>

namespace pure_pursuit {
void PurePursuit::set_path(Path path) {
    path_ = path;
    setted_flag_ = true;
    path_count_ = 0;
};

void PurePursuit::start_tracking() {
    if (!setted_flag_) {
        std::cout << "please set path" << std::endl;
        return;
    }
    tracking_flag_ = true;
};

void PurePursuit::calculate(diff2_odometry::Pose current_pose) {
    auto& current_point = current_pose.point;
    auto& current_theta = current_pose.theta;
    if (setted_flag_ && tracking_flag_) {
        target_point_ = path_.points[path_count_];
        const auto delta_length = sqrt((target_point_.x - current_point.x) * (target_point_.x - current_point.x) +
                                       (target_point_.y - current_point.y) * (target_point_.y - current_point.y));
        const auto delta_theta =
            atan2(target_point_.y - current_point.y, target_point_.x - current_point.x) - current_theta;
        // std::cout << "in PurePursuit" << std::endl
        //           << "target_point_.x: " << target_point_.x << " target_point_.y: " << target_point_.y << std::endl
        //           << "current_point.x: " << current_point.x << " current_point.y: " << current_point.y
        //           << " current_theta: " << current_theta << std::endl
        //           << "delta_length: " << delta_length << " abs length: " << std::abs(delta_length)
        //           << " delta_theta: " << delta_theta << std::endl
        //           << "path_count_: " << path_count_ << std::endl;

        if (point_is_equal(target_point_, path_.points.back())) {  // if target point is goal point
            if (std::abs(delta_length) < config_.tolerance) {
                output_.left = 0;
                output_.right = 0;
                tracking_flag_ = false;
                std::cout << "finish tracking" << std::endl;
                return;
            }
        } else if (std::abs(delta_length) < config_.lookahead_length) {  // robot is near target point
            path_count_++;
            std::cout << "next target point" << std::endl;
            return;
        }
        const auto tmp_left_output = config_.vel_gain * delta_length - config_.omega_gain * delta_theta;
        const auto tmp_right_output = config_.vel_gain * delta_length + config_.omega_gain * delta_theta;
        output_.left = util::limit(tmp_left_output, -config_.vel_limit, config_.vel_limit);
        output_.right = util::limit(tmp_right_output, -config_.vel_limit, config_.vel_limit);
        // std::cout << "tmp_left_output: " << tmp_left_output << " tmp_right_output: " << tmp_right_output << std::endl
        //           << "output_.left: " << output_.left << " output_.right: " << output_.right << std::endl;
    }
}
}  // namespace pure_pursuit
#pragma once
#include <cstdint>

namespace roomba {
namespace open_interfaces {

    namespace started_commands {
        inline static constexpr uint8_t start = 128;  // Open Interfacesをスタートさせる
        inline static constexpr uint8_t reset = 7;    // ロボットをリセットする
        inline static constexpr uint8_t stop = 173;   // Open Interfaceを停止させる
        inline static constexpr uint8_t baud = 129;   // ボーレートを変更する
    }                                                 // namespace started_commands

    namespace mode_commands {
        inline static constexpr uint8_t safe = 131;  // セーフモードにする
        inline static constexpr uint8_t full = 132;  // フルモードにする
    }                                                // namespace mode_commands

    namespace cleaning_commands {
        inline static constexpr uint8_t clean = 135;
        inline static constexpr uint8_t max = 136;
        inline static constexpr uint8_t spot = 134;
        inline static constexpr uint8_t seek_dock = 143;
        inline static constexpr uint8_t power = 133;
    }  // namespace cleaning_commands

    namespace actuator_commands {
        inline static constexpr uint8_t drive = 137;
        inline static constexpr uint8_t drive_direct = 145;
        inline static constexpr uint8_t drive_pwm = 146;
        inline static constexpr uint8_t motors = 138;
        inline static constexpr uint8_t pwm_motors = 144;
        inline static constexpr uint8_t leds = 139;
        inline static constexpr uint8_t song = 140;
        inline static constexpr uint8_t play = 141;
    }  // namespace actuator_commands

    namespace input_commands {
        inline static constexpr uint8_t sensors = 142;
        inline static constexpr uint8_t query_list = 149;
        inline static constexpr uint8_t stream = 148;
    }  // namespace input_commands

    namespace sensor_packets {
        inline static constexpr uint8_t bump_wheeldrop = 7;
        inline static constexpr uint8_t left_encoder_counts = 43;
        inline static constexpr uint8_t right_encoder_counts = 44;
        inline static constexpr uint8_t lifht_bumper = 45;
        inline static constexpr uint8_t light_bump_left = 46;
        inline static constexpr uint8_t light_bump_front_left = 47;
        inline static constexpr uint8_t light_bump_center_lef = 48;
        inline static constexpr uint8_t light_bump_center_right = 49;
        inline static constexpr uint8_t light_bump_front_right = 50;
        inline static constexpr uint8_t light_bump_right = 51;
        inline static constexpr uint8_t left_motor_current = 54;
        inline static constexpr uint8_t right_motor_current = 55;
        inline static constexpr uint8_t main_brush_motor_current = 56;
        inline static constexpr uint8_t side_brush_motor_current = 57;
    }  // namespace sensor_packets
}  // namespace open_interfaces
}  // namespace roomba
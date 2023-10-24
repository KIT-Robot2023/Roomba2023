#pragma once
#include "roomba_open_interface.hpp"
#include "serial.h"
#include "songs.hpp"

namespace roomba {
class Command {
public:
    Command() = default;
    ~Command() = default;
    Command(serial &serial, char *com_port_name)
        : serial_(serial), com_port_name_(com_port_name), serial_port_ready_(false){};
    bool init();
    void send_one_command(const uint8_t cmd);
    void send_start_command();
    void send_stop_command();
    void send_reset_command();
    void send_full_mode_command();
    void send_safe_mode_command();
    void send_drive_direct_command(int left_motor_vel, int right_motor_vel);
    void send_drive_pwm_command(int left_motor_value, int right_motor_value);
    void send_pwm_motors_command(int main_brush_pwm, int side_brush_pwm, int vacuum_pwm);
    int send_seek_dock_command();
    int send_led_command(char led_color, char led_brightness);  // 未検証
    int send_song_command(roomba::music::SongBase &song);
    int send_play_command(uint8_t song_number);
    int receive_message(int byte);
    int receive_initial_message();
    int get_encoder_left();
    int get_encoder_right();
    char get_lifht_bumper_response();
    int get_light_bumper_left();
    int get_light_bumper_front_left();
    int get_light_bumper_center_left();
    int get_light_bumper_center_right();
    int get_light_bumper_front_right();
    int get_light_bumper_right();

    char get_sensors();

private:
    serial &serial_;
    char *com_port_name_;
    char send_buffer_[64];      // ルンバ送信バッファ
    char receive_buffer_[512];  // ルンバ受信バッファ
    bool serial_port_ready_;
    void comport_scan_();
    bool serial_port_init_();
    int joint_high_low_byte_(int hbyte, int lbyte);
    char set_drive_command_(char *buf_out, int left_motor_pwm, int right_motor_pwm);
    char get_sensor_1B_(int sensor_no);
    char get_sensor_2B_(int sensor_no);
};
}  // namespace roomba
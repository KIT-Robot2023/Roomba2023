#include "../include/roomba_command.hpp"

#include <chrono>
#include <iostream>

namespace roomba {
bool Command::init() {
    bool result = false;
    std::cout << "init().." << std::endl;
    comport_scan_();
    result = serial_port_init_();
    if (result) {
        serial_port_ready_ = true;
        std::cout << "Done." << std::endl;
    } else {
        serial_port_ready_ = false;
        std::cout << "Error." << std::endl;
    }
    return result;
}

void Command::send_one_command(const uint8_t cmd_in) {
    uint8_t sbuf[64];
    sbuf[0] = cmd_in;  // 1バイト分セット．usigned charに型セット
    printf("send_command: %d\n", sbuf[0]);
    serial_.send(sbuf, 1);  // コマンド送信
}

void Command::send_start_command() { send_one_command(open_interfaces::started_commands::start); }

void Command::send_stop_command() { send_one_command(open_interfaces::started_commands::stop); }

void Command::send_reset_command() { send_one_command(open_interfaces::started_commands::reset); }

void Command::send_full_mode_command() { send_one_command(open_interfaces::mode_commands::full); }

void Command::send_safe_mode_command() { send_one_command(open_interfaces::mode_commands::safe); }

void Command::send_drive_pwm_command(int left_pwm, int right_pwm) {
    uint8_t byte = 5;
    char *sbuf = send_buffer_;
    uint8_t index = 0;

    sbuf[index++] = open_interfaces::actuator_commands::drive_pwm;  // コマンド

    if ((-255 <= left_pwm && left_pwm <= 255) && (-255 <= right_pwm && right_pwm <= 255)) {
        int LHbyte = left_pwm & 0xff00;
        LHbyte = (LHbyte >> 8);
        int LLbyte = left_pwm & 0x00ff;
        int RHbyte = right_pwm & 0xff00;
        RHbyte = (RHbyte >> 8);
        int RLbyte = right_pwm & 0x00ff;

        sbuf[index++] = (unsigned char)LHbyte;
        sbuf[index++] = (unsigned char)LLbyte;
        sbuf[index++] = (unsigned char)RHbyte;
        sbuf[index++] = (unsigned char)RLbyte;

        serial_.send(sbuf, byte);
    } else {
        std::cout << "in drive pwm command, pwm value is out of range" << std::endl;
    }
}

void Command::send_drive_direct_command(int left_motor_vel, int right_motor_vel) {
    uint8_t byte = 5;
    char *sbuf = send_buffer_;
    uint8_t index = 0;

    sbuf[index++] = open_interfaces::actuator_commands::drive_direct;  // コマンド

    if ((-500 <= left_motor_vel && left_motor_vel <= 500) && (-500 <= right_motor_vel && right_motor_vel <= 500)) {
        int LHbyte = left_motor_vel & 0xff00;
        LHbyte = (LHbyte >> 8);
        int LLbyte = left_motor_vel & 0x00ff;
        int RHbyte = right_motor_vel & 0xff00;
        RHbyte = (RHbyte >> 8);
        int RLbyte = right_motor_vel & 0x00ff;

        sbuf[index++] = (unsigned char)LHbyte;
        sbuf[index++] = (unsigned char)LLbyte;
        sbuf[index++] = (unsigned char)RHbyte;
        sbuf[index++] = (unsigned char)RLbyte;

        serial_.send(sbuf, byte);
    } else {
        std::cout << "in drive direct command, motor velocity value is out of range" << std::endl;
    }
}

void Command::send_pwm_motors_command(int main_brush_pwm, int side_brush_pwm, int vacuum_pwm) {
    uint8_t byte = 4;
    char *sbuf = send_buffer_;
    sbuf[0] = open_interfaces::actuator_commands::pwm_motors;  // コマンド
    sbuf[1] = main_brush_pwm;                                  // メインブラシ-127～+127
    sbuf[2] = side_brush_pwm;                                  // サイドブラシ-127～+127
    sbuf[3] = vacuum_pwm;                                      // 吸引 0～+127
    serial_.send(sbuf, byte);
}

int Command::send_seek_dock_command() { send_one_command(open_interfaces::cleaning_commands::seek_dock); }

int Command::send_led_command(char led_color, char led_brightness) {
    uint8_t byte = 4;
    char *sbuf = send_buffer_;

    sbuf[0] = open_interfaces::actuator_commands::leds;
    sbuf[1] = 0xf;  // LEDの数
    sbuf[2] = led_color;
    sbuf[3] = led_brightness;
    serial_.send(sbuf, byte);  // コマンド送信．LED点灯

    return byte;
}

int Command::send_song_command(roomba::music::SongBase &song) {
    uint8_t byte = 2 * song.song_notes().size() + 2;
    char *sbuf = send_buffer_;

    sbuf[0] = open_interfaces::actuator_commands::song;
    sbuf[1] = song.song_number();

    for (int i = 2; i < byte; i++) {
        if (i % 2 == 0) {
            sbuf[i] = song.song_notes()[i - 2].name;
            sbuf[i + 1] = song.song_notes()[i - 2].duration;
        }
    }

    serial_.send(sbuf, byte);  // コマンド送信
    return byte;
}

int Command::send_play_command(uint8_t song_number) {
    int byte = 2;
    char *sbuf = send_buffer_;

    sbuf[0] = open_interfaces::actuator_commands::play;
    sbuf[1] = song_number;

    serial_.send(sbuf, byte);  // コマンド送信．
    return byte;
}

int Command::receive_message(int byte) {
    // メッセージなど受信
    char *rbuf = receive_buffer_;
    // int res=s->receive(rbuf,byte);
    int res = serial_.receive3(rbuf, byte);
    if (res < 1) {
        printf("Error receive_message()\n");
        return 0;
    }
    printf("receive_message(%s)\n", com_port_name_);
    printf("---------------\n");
    printf("%s", rbuf);
    printf("\n---------------\n");
    printf("[%d byte]\n", res);
    return 1;
}

int Command::receive_initial_message() {
    // 初期メッセージ受信
    char rbuf[512];
    for (int i = 0; i < 512; i++) rbuf[i] = '\0';  // ゼロを詰める
    int res_byte;
    int pos = 0;  // バッファ中の位置
    serial_.purge();
    res_byte = serial_.receive3(rbuf, 234);  // まず234バイト読み込み
    if (res_byte < 1) {
        printf("Error receive_message()\n");
        return 0;
    }
    pos = res_byte;
    res_byte = serial_.receive3(rbuf + pos, 256);  // 続きの読み込み（ない場合もあり）
    if (res_byte < 1) {
        // printf("Error receive_message()\n");
        // return 0;
        ;
    }
    printf("receive_message(%s)\n", com_port_name_);
    printf("---------------\n");
    printf("%s", rbuf);
    printf("\n---------------\n");
    printf("[%d byte]\n", pos + res_byte);
    return 1;
}

int Command::get_encoder_left() { return get_sensor_2B_(open_interfaces::sensor_packets::left_encoder_counts); }

int Command::get_encoder_right() { return get_sensor_2B_(open_interfaces::sensor_packets::right_encoder_counts); }

char Command::get_lifht_bumper_response() { return get_sensor_1B_(open_interfaces::sensor_packets::lifht_bumper); }

int Command::get_light_bumper_left() { return get_sensor_2B_(open_interfaces::sensor_packets::light_bump_front_left); }

int Command::get_light_bumper_front_left() {
    return get_sensor_2B_(open_interfaces::sensor_packets::light_bump_front_left);
}

int Command::get_light_bumper_center_left() {
    return get_sensor_2B_(open_interfaces::sensor_packets::light_bump_front_left);
}

int Command::get_light_bumper_center_right() {
    return get_sensor_2B_(open_interfaces::sensor_packets::light_bump_center_right);
}

int Command::get_light_bumper_front_right() {
    return get_sensor_2B_(open_interfaces::sensor_packets::light_bump_front_right);
}

int Command::get_light_bumper_right() { return get_sensor_2B_(open_interfaces::sensor_packets::light_bump_right); }

char Command::get_sensors() {
    // if (serial_port_ready_ != true) return -1;  // ポート準備ができていなければ処理しない．

    // RoombaSensor *rss = &roomba[port_in].sensor;

    // s->purge();  // シリアル通信のバッファクリア

    // rss->stat = get_sensor_1B(58, port_in);
    // rss->EncL = get_sensor_2B(43, port_in);
    // rss->EncR = get_sensor_2B(44, port_in);
    // rss->LBumper = get_sensor_1B(45, port_in);
    // rss->LBumper_L = get_sensor_2B(46, port_in);
    // rss->LBumper_FL = get_sensor_2B(47, port_in);
    // rss->LBumper_CL = get_sensor_2B(48, port_in);
    // rss->LBumper_CR = get_sensor_2B(49, port_in);
    // rss->LBumper_FR = get_sensor_2B(50, port_in);
    // rss->LBumper_R = get_sensor_2B(51, port_in);
    // rss->Angle = get_sensor_2B(20, port_in);     // 値が怪しい
    // rss->Distance = get_sensor_2B(19, port_in);  // 値が怪しい.ゼロしか出ない

    // mstime2 = get_millisec();
    // rss->TimeNow = mstime2 - mstime1;  // 現在時刻 201101 clock_gettime()使用

    return 1;
}
/*----------------------------------------------- private --------------------------------------------------*/

void Command::comport_scan_() {
    char port_str[128];
    bool res;

    printf("COM port scanning. Available ports: ...\n");
    for (int i = 1; i <= 32; i++) {
        sprintf(port_str, "\\\\.\\COM%d", i);  // for windows
        // sprintf(port_str,"/dev/ttyS%d",i); //for linux
        res = serial_.init(port_str, 115200);  // 初期化
        if (res == true) {
            printf("[%s]\n", port_str);
            serial_.close();
        }
    }
    printf("Done.\n");
}

bool Command::serial_port_init_() {
    // シリアルポート初期化
    bool res;

    res = serial_.init(com_port_name_, 115200);  // 初期化
    serial_.purge();                             // バッファクリア
    if (res != true) {
        printf("Port Open Error#0 [%s]\n", com_port_name_);
    } else {
        printf("Port[%s] Ready.\n", com_port_name_);
    }
    return res;
}

int Command::joint_high_low_byte_(int hbyte, int lbyte) {
    int result = 0;
    result = (hbyte << 8) | lbyte;
    return result;
}

char Command::set_drive_command_(char *buffer_out, int left_pwm, int right_pwm) {
    int LHbyte = left_pwm & 0xff00;
    LHbyte = (LHbyte >> 8);
    int LLbyte = left_pwm & 0x00ff;
    int RHbyte = right_pwm & 0xff00;
    RHbyte = (RHbyte >> 8);
    int RLbyte = right_pwm & 0x00ff;

    buffer_out[0] = (unsigned char)LHbyte;
    buffer_out[1] = (unsigned char)LLbyte;
    buffer_out[2] = (unsigned char)RHbyte;
    buffer_out[3] = (unsigned char)RLbyte;

    return 1;
}

char Command::get_sensor_1B_(int sensor_no) {
    // 1バイトセンサデータ受信
    if (serial_port_ready_ != true) return -1;  ////ポート準備ができていなければ処理しない．

    char *sbuf = send_buffer_;
    char *rbuf = receive_buffer_;

    char db = -1;  // databyte

    // センサ情報取得
    // 送信要求
    sbuf[0] = open_interfaces::input_commands::sensors;  // コマンド
    sbuf[1] = (unsigned char)sensor_no;                  // センサ番号
    serial_.send(sbuf, 2);

    // printf("get_sensor_1B(%d) -- ",sensor_no);
    // 受信
    int res = serial_.receive(rbuf, 1);
    if (res < 1) {
        printf("Error get_sensor_1B()\n");
        return 0;
    }

    char b = rbuf[0];
    // printf("[0x%x]=[%d] \n", b,b);

    db = b;
    return db;
}

char Command::get_sensor_2B_(int sensor_no) {
    // 2バイト(int)センサデータ受信
    if (serial_port_ready_ != true) return -1;  ////ポート準備ができていなければ処理しない．

    char *sbuf = send_buffer_;
    char *rbuf = receive_buffer_;

    int dat = -1;  // databyte
    // センサ情報取得
    // 送信要求
    sbuf[0] = open_interfaces::input_commands::sensors;  // コマンド
    sbuf[1] = (unsigned char)sensor_no;                  // センサ番号
    serial_.send(sbuf, 2);

    // printf("get_sensor_2B(%d) -- ", sensor_no);
    // 受信
    int res = serial_.receive(rbuf, 2);
    if (res < 2) {
        printf("Error get_sensor_2B()\n");
        return 0;
    }

    int hbyte = rbuf[0];
    int lbyte = rbuf[1];
    // printf("H[0x%x]:L[0x%x]  -- val[%d]\n", hbyte, lbyte, val);

    dat = joint_high_low_byte_(hbyte, lbyte);

    return dat;
}

}  // namespace roomba
#include <climits>
#include <cstdio>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <thread>

#include "include/kbhit.hpp"
#include "include/roomba.hpp"
#include "include/roomba_command.hpp"
#include "include/roomba_open_interface.hpp"
#include "include/timer.hpp"

// #define VERTIAL

using std::chrono::duration_cast;
using std::chrono::milliseconds;
using std::chrono::steady_clock;

int main() {
    const steady_clock::time_point system_start_time = steady_clock::now();
    Timer ctrl_timer;
    ctrl_timer(milliseconds(50), true);
    Timer key_input_timer;
    key_input_timer(milliseconds(1), true);
    Timer disp_timer;
    disp_timer(milliseconds(100), true);
    Timer log_timer;
    log_timer(milliseconds(50), true);

    const std::string log_file_name = "./logfiles\\" + util::get_date_and_time() + ".csv";
    std::ofstream log_file(log_file_name);
    if (!log_file.is_open()) {
        std::cout << "failed to open log file" << std::endl;
        return 1;
    } else {
        std::cout << "log file opened" << std::endl;
        std::cout << "log file name: " << log_file_name << std::endl;
        std::cout << "write log file header" << std::endl;
        log_file << "time,odo_x,odo_y,odo_theta,odo_v,odo_w,enc_left,enc_right" << std::endl;
    }

    serial serial;
    roomba::Command roomba_command(serial, "\\\\.\\COM10");
    diff2_odometry::Diff2OdometryConfig odo_config(508, USHRT_MAX, 0.036, 0.235);
#ifdef VERTIAL
    diff2_odometry::VertialDiff2Odometry odometry(odo_config);
    roomba::VertialRoomba roomba(odometry);
#else
    diff2_odometry::Diff2Odometry odometry(roomba_command, odo_config);
    roomba::Roomba roomba(roomba_command, odometry);
#endif
    roomba.init();

    while (true) {
        if (key_input_timer()) {
            int base_vel = 200;  // mm/s
            if (key::kbhit()) {
                const unsigned char key = getch();
                switch (key) {
                case 'w': roomba.drive(base_vel, base_vel); break;
                case 'a': roomba.drive(base_vel, -base_vel); break;
                case 's': roomba.drive(-base_vel, -base_vel); break;
                case 'd': roomba.drive(-base_vel, base_vel); break;
                case 'q': roomba.drive(base_vel, base_vel / 4.0); break;
                case 'e': roomba.drive(base_vel / 4.0, base_vel); break;
                case 'z': roomba.drive(-base_vel, -base_vel / 4.0); break;
                case 'c': roomba.drive(-base_vel / 4.0, -base_vel); break;
                case 0x20: roomba.drive(0, 0);
                default: break;
                }
            }
        }
        if (ctrl_timer()) { roomba.cycle(); }
        if (disp_timer()) {
            // std::cout << "current time: "
            //           << duration_cast<milliseconds>(steady_clock::now() - system_start_time).count()
            //           << " odo x: " << roomba.odo().x << "  y: " << roomba.odo().y << "  z: " << roomba.odo().theta
            //           << "  v: " << roomba.odo().y << "  w: " << roomba.odo().w << std::endl;
        }
        if (log_timer()) {
            std::ostringstream oss;
            oss << std::fixed << std::setprecision(8)
                << duration_cast<milliseconds>(steady_clock::now() - system_start_time).count() << "," << roomba.odo().x
                << "," << roomba.odo().y << "," << roomba.odo().theta << "," << roomba.odo().v << "," << roomba.odo().w
                << "," << odometry.encoder_left() << "," << odometry.encoder_right() << std::endl;
            log_file << oss.str();
            // std::cout << oss.str();
        }
    }

    return 0;
}
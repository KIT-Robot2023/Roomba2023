#include <climits>
#include <cmath>
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
        log_file << "time,odo_x,odo_y,odo_theta,odo_v,odo_w,enc_left,enc_right,target_x, target_y" << std::endl;
    }

    serial serial;
    roomba::Command roomba_command(serial, "\\\\.\\COM7");
    diff2_odometry::Diff2OdometryConfig odo_config(508, USHRT_MAX, 0.036, 0.235);
    diff2_odometry::Diff2Odometry odometry(roomba_command, odo_config);
    pure_pursuit::PurePursuitConfig pure_pursuit_config(1.0, 1.0, 500.0 / 1000, 150.0 / 1000.0, 5.0 / 1000.0);
    pure_pursuit::PurePursuit pure_pursuit(pure_pursuit_config);
    roomba::Roomba roomba(roomba_command, odometry, pure_pursuit);
    // path
    pure_pursuit::Path path1;
    for (float i = 0; i < 2; i += 0.01) {
        const double x = i;
        const double y = 0.5 * sin(util::pi_d * i);
        path1.points.push_back(diff2_odometry::Point(x, y));
    }
    pure_pursuit::Path path2;
    roomba.init();

    bool roomba_init_flag = false;
    bool setting_flag = false;

    while (true) {
        while (!roomba_init_flag) {
            std::cout << "===== waiting for roomba init ===== \n"
                      << "type <start> is send start\n"
                      << "type <reset> is send reset command\n"
                      << "type <stop> is send stop\n"
                      << "type <safe> is set safe mode\n"
                      << "type <full> is set full mode\n"
                      << "please type command: ";
            std::string command;
            std::cin >> command;

            if (command == "start") {
                std::cout << "send start mode\n" << std::endl;
                roomba.set_mode(roomba::open_interfaces::started_commands::start);
                roomba_init_flag = false;
                break;
            } else if (command == "reset") {
                std::cout << "send reset command\n" << std::endl;
                roomba.set_mode(roomba::open_interfaces::started_commands::reset);
                return 0;
                break;
            } else if (command == "stop") {
                std::cout << "send stop mode\n" << std::endl;
                roomba.set_mode(roomba::open_interfaces::started_commands::stop);
                roomba_init_flag = false;
                break;
            } else if (command == "safe") {
                std::cout << "send safe mode\n" << std::endl;
                roomba.set_mode(roomba::open_interfaces::mode_commands::safe);
                roomba_init_flag = true;
                break;
            } else if (command == "full") {
                std::cout << "send full mode\n" << std::endl;
                roomba.set_mode(roomba::open_interfaces::mode_commands::full);
                roomba_init_flag = true;
                break;
            } else {
                std::cout << "error: invalid command" << std::endl;
            }
        }

        while (roomba_init_flag == true && !setting_flag) {
            std::cout << "===== waiting for system setting ===== \n"
                      << "type <manual> is reset path\n"
                      << "type <auto> is exit setting\n"
                      << "please type command: ";
            std::string command;
            std::cin >> command;
            if (command == "manual") {
                std::cout << "start manual moving\n" << std::endl;
                setting_flag = true;
                break;
            } else if (command == "auto") {
                std::cout << "start tracking\n" << std::endl;
                setting_flag = true;
                roomba.set_path(path1);
                roomba.start_path_tracking();
                break;
            } else {
                std::cout << "error: invalid command" << std::endl;
            }
        }

        if (key_input_timer()) {
            double base_vel = 200.0 / 1000.0;  // m/s
            if (key::kbhit()) {
                const unsigned char key = getch();
                switch (key) {
                case 'w': roomba.drive(base_vel, base_vel); break;
                case 'a': roomba.drive(-base_vel, base_vel); break;
                case 's': roomba.drive(-base_vel, -base_vel); break;
                case 'd': roomba.drive(base_vel, -base_vel); break;
                case 'q': roomba.drive(base_vel / 4.0, base_vel); break;
                case 'e': roomba.drive(base_vel, base_vel / 4.0); break;
                case 'z': roomba.drive(-base_vel / 4.0, -base_vel); break;
                case 'c': roomba.drive(-base_vel, -base_vel / 4.0); break;
                case 0x20: roomba.drive(0, 0); break;
                case 0x1b:  // esc
                    std::cout << "change system to init" << std::endl;
                    roomba.drive(0.0, 0.0);
                    roomba.set_system_mode(roomba::Roomba::SystemMode::init);
                    roomba_init_flag = false;
                    setting_flag = false;
                    break;
                default: break;
                }
            }
        }
        if (ctrl_timer()) { roomba.cycle(); }
        if (disp_timer()) {
            using namespace std;
            // cout << "==== roomba system ====" << endl << "sytem mode :" << static_cast<int>(roomba.system_mode) <<
            // endl; std::cout << "current time: "
            //           << duration_cast<milliseconds>(steady_clock::now() - system_start_time).count()
            //           << " odo x: " << roomba.odo().x << "  y: " << roomba.odo().y << "  z: " <<
            //           roomba.odo().theta
            //           << "  v: " << roomba.odo().y << "  w: " << roomba.odo().w << std::endl;
        }
        if (log_timer()) {
            std::ostringstream oss;
            oss << std::fixed << std::setprecision(8)
                << duration_cast<milliseconds>(steady_clock::now() - system_start_time).count() << ","
                << roomba.odo().pose.point.x << "," << roomba.odo().pose.point.y << "," << roomba.odo().pose.theta
                << "," << roomba.odo().twist.v << "," << roomba.odo().twist.w << "," << odometry.encoder_left() << ","
                << odometry.encoder_right() << "," << pure_pursuit.target_point().x << ","
                << pure_pursuit.target_point().y << std::endl;
            log_file << oss.str();
            // std::cout << oss.str();
        }
    }

    return 0;
}
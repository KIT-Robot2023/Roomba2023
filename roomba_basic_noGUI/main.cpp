#include <limits.h>

#include <cstdio>
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
    ctrl_timer(milliseconds(100), true);
    Timer key_input_timer;
    key_input_timer(milliseconds(1), true);
    Timer disp_timer;
    disp_timer(milliseconds(200), true);

    serial serial;
    roomba::Command roomba_command(serial, "\\\\.\\COM12");
    diff2_odometry::Diff2OdometryConfig odo_config(508, 0.036, 0.235);
    diff2_odometry::Diff2Odometry odometry(roomba_command, odo_config);
    roomba::Roomba roomba(roomba_command, odometry);
    roomba.init();

    while (true) {
        if (key_input_timer()) {
            if (key::kbhit()) {
                const unsigned char key = getch();
                int base_vel = 200;
                switch (key) {
                case 'w': roomba.drive(base_vel, base_vel); break;
                case 'a': roomba.drive(base_vel, -base_vel); break;
                case 's': roomba.drive(-base_vel, -base_vel); break;
                case 'd': roomba.drive(-base_vel, base_vel); break;
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
    }

    return 0;
}
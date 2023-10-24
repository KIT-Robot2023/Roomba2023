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
    ctrl_timer(milliseconds(10), true);
    Timer key_input_timer;
    key_input_timer(milliseconds(100), true);

    serial serial;
    roomba::Command roomba_command(serial, "\\\\.\\COM10");
    roomba::Roomba roomba(roomba_command);
    roomba.init();

    while (true) {
        if (key_input_timer()) {
            if (key::kbhit()) {
                const unsigned char key = getch();
                switch (key) {
                case 'w': std::cout << "<w> pressed." << std::endl; break;
                case 'a': std::cout << "<a> pressed. " << std::endl; break;
                case 's': std::cout << "<s> pressed." << std::endl; break;
                case 'd': std::cout << "<d> pressed." << std::endl; break;
                default: break;
                }
            }
        }
        if (ctrl_timer()) {
            roomba.cycle();
            std::cout << "current time: "
                      << duration_cast<milliseconds>(steady_clock::now() - system_start_time).count()
                      << " encL: " << roomba.sensors().enc_left << " encR: " << roomba.sensors().enc_right << std::endl;
        }
    }

    return 0;
}
#include "roomba_command.hpp"

namespace odometry {
class Diff2Odometry {
public:
    Diff2Odometry(roomba::Command &roomba_command) : roomba_command_(roomba_command){};

private:
    roomba::Command &roomba_command_;
};
}  // namespace odometry
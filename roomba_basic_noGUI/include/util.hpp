#pragma once
#include <iomanip>
#include <sstream>
#include <string>

namespace util {
inline static constexpr double pi_d = 3.1415926535897932384626433832795;
inline static constexpr float pi_f = static_cast<float>(pi_d);

template <class T>
constexpr int sign(T a) {
    return a >= 0 ? 1 : -1;
}

inline std::string get_date_and_time() {
    using namespace std;
    time_t t = time(nullptr);
    const tm* localTime = localtime(&t);
    std::stringstream s;
    s << localTime->tm_year + 1900;
    s << "-" << setw(2) << setfill('0') << localTime->tm_mon + 1;
    s << "-" << setw(2) << setfill('0') << localTime->tm_mday;
    s << "__" << setw(2) << setfill('0') << localTime->tm_hour;
    s << "-" << setw(2) << setfill('0') << localTime->tm_min;
    s << "-" << setw(2) << setfill('0') << localTime->tm_sec;
    return s.str();
}

inline constexpr double limit(double target, double min, double max) {
    if (target < min)
        return min;
    else if (max < target)
        return max;
    else
        return target;
}
}  // namespace util
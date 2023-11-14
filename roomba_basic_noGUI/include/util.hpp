#pragma once


namespace util {
inline static constexpr double pi_d = 3.1415926535897932384626433832795;
inline static constexpr float pi_f = static_cast<float>(pi_d);

template <class T>
constexpr int sign(T a) { return a >= 0 ? 1 : -1;}

}  // namespace util
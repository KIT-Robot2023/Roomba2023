#pragma once
#include <cstdint>
#include <vector>

namespace roomba {
namespace music {

    enum NoteName {
        // clang-format off
        G0 = 31, Gs0 = 32, A0 = 33, As0 = 34, B0 = 35, C0 = 36, Cs0 = 37, D0 = 38, Ds0 = 39, E0 = 40, F0 = 41, Fs0 = 42, 
        G1 = 43, Gs1 = 44, A1 = 45, As1 = 46, B1 = 47, C1 = 48, Cs1 = 49, D1 = 50, Ds1 = 51, E1 = 52, F1 = 53, Fs1 = 54,
        G2 = 55, Gs2 = 56, A2 = 57, As2 = 58, B2 = 59, C2 = 60, Cs2 = 61, D2 = 62, Ds2 = 63, E2 = 64, F2 = 65, Fs2 = 66,
        G3 = 67, Gs3 = 68, A3 = 69, As3 = 70, B3 = 71, C3 = 72, Cs3 = 73, D3 = 74, Ds3 = 75, E3 = 76, F3 = 77, Fs3 = 78,
        G4 = 79, Gs4 = 80, A4 = 81, As4 = 82, B4 = 83, C4 = 84, Cs4 = 85, D4 = 86, Ds4 = 87, E4 = 88, F4 = 89, Fs4 = 90,
        G5 = 91, Gs5 = 92, A5 = 93, As5 = 94, B5 = 95, C5 = 96, Cs5 = 97, D5 = 98, Ds5 = 99, E5 = 100,F5 = 101,Fs5 = 102,
        G6 = 103,Gs6 = 104,A6 = 105,As6 = 106,B6 = 107,
        // clang-format on
    };

    enum NoteDuration {
        OneSecond = 64,
    };

    struct Note {
        Note() = default;
        ~Note() = default;
        Note(NoteName name, uint8_t duration) : name(name), duration(duration) {}
        NoteName name;
        uint8_t duration;
    };

}  // namespace music

}  // namespace roomba
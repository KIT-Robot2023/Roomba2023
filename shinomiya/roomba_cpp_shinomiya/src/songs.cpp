#include "../include/songs.hpp"

namespace roomba {
using namespace roomba::music;
FamilyMart::FamilyMart() {
    std::vector<Note> song_notes = {
        // clang-format off
        Note(Fs4, 1 / 4 * OneSecond),
        Note(D4, 1 / 4 * OneSecond),
        Note(A4, 1 / 4 * OneSecond),
        Note(D4, 1 / 4 * OneSecond),
        Note(E4, 1 / 4 * OneSecond),
        Note(A5, 3 / 4 * OneSecond),
        Note(E4, 1 / 4 * OneSecond),
        Note(Fs4, 1 / 4 * OneSecond),
        Note(E4, 1 / 4 * OneSecond),
        Note(A4, 1 / 4 * OneSecond),
        Note(D4, 3 / 4 * OneSecond),
        // clang-format on
    };
    song_notes_ = song_notes;
};
}  // namespace roomba
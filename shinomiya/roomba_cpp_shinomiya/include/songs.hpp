#include "song_base.hpp"

namespace roomba {
class FamilyMart : public roomba::music::SongBase {
public:
    FamilyMart();
    uint8_t song_number() override { return song_number_; };
    std::vector<roomba::music::Note>& song_notes() override { return song_notes_; };

private:
    uint8_t song_number_ = 0;
    std::vector<roomba::music::Note> song_notes_;
};
}  // namespace roomba
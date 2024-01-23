#include "roomba_music.hpp"

namespace roomba {
namespace music {

    class SongBase {
    public:
        virtual uint8_t song_number() = 0;
        virtual std::vector<roomba::music::Note>& song_notes() = 0;
    };

}  // namespace music
}  // namespace roomba
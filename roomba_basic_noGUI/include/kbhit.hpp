// #define LINUX //Linuxの場合こちらだけ有効
#define WIN32  // Windowsの場合こちらだけ有効

#ifdef WIN32
#undef LINUX
#include <conio.h>
#include <windows.h>

namespace key {
int kbhit() { return _kbhit(); }
}  // namespace key
#endif

#ifdef LINUX
#undef WIN32
#include <fcntl.h>
#include <stdio.h>
#include <termios.h>
#include <unistd.h>
namespace key {
int kbhit(void) {
    struct termios oldt, newt;
    int ch;
    int oldf;

    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

    ch = getchar();

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, oldf);

    if (ch != EOF) {
        ungetc(ch, stdin);
        return 1;
    }
    return 0;
}
}  // namespace key
#endif

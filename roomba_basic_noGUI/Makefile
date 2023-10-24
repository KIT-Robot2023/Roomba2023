CC = g++
CC_MINGW64VSC = c:\mingw64\bin\g++.exe
CXXFLAGS    = -Wall -Wextra -std=c++17
SAMPLE = src/roomba_test.cpp src/serial.cpp
SRC = main.cpp src/serial.cpp src/roomba.cpp src/roomba_command.cpp src/songs.cpp
WIN_LIB32 := mingw32_lib/libfreeglut/libfreeglut.a
WIN_LIB64 := mingw32_lib/libfreeglut/x64/freeglut.lib
WIN_OPT = -lglu32 -lm -lopengl32 -static -lstdc++ -lgcc  -lwinpthread

all:win64

win64:
	$(CC_MINGW64VSC) -o roomba_test_d.exe $(SAMPLE)  $(WIN_OPT) 
	$(CC_MINGW64VSC) $(CXXFLAGS) -o roomba.exe $(SRC)  $(WIN_OPT) 

linux:
	$(CC) -o roomba_test_d.exe $(SRC) -L/usr/lib  -lm 

linux-glut:
	$(CC) -o roomba_test_d.exe $(SRC) -L/usr/lib -lglut -lGLU -lGL -lm 

clean:
	rm *.o *.exe

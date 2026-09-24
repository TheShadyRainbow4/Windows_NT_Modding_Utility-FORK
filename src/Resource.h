#pragma once

#define STRINGIZE_(s) #s
#define STRINGIZE(s)  STRINGIZE_(s)

#define VER_MAJOR                2
#define VER_MINOR                10
#define VER_REVISION             20
#define VER_BUILD                20

#define VER_STRING \
    STRINGIZE(VER_MAJOR) "." STRINGIZE(VER_MINOR) "." STRINGIZE(VER_BUILD) "." STRINGIZE(VER_REVISION)

#define IDI_NTMU               100
#define IDI_ABOUT              101
#define IDR_COMPLETE_WAV       102
#define IDR_WAV_COMPLETE       200


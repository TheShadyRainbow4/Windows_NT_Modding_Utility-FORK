#pragma once
#include <wchar.h>
#include <stdio.h>

#define MM_DEC extern
#define MM_IMPL
#define MM_FORMATTED_STRING_BODY_W(fmt, ...) { \
    static __declspec(thread) wchar_t buf[1024]; \
    swprintf_s(buf, 1024, fmt, __VA_ARGS__); \
    return buf; \
}

namespace msgmap {
    typedef wchar_t* wstring;
}

typedef struct _mm_translation_mapping_t {
    void *translations;
    const char *lang;
    const char *region;
} mm_translation_mapping_t;

inline void mm_set_preferred_langs_from_system(void) {}

inline const void *mm_get_translations(const mm_translation_mapping_t *map, int count) {
    return map[0].translations;
}

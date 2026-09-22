#include <windows.h>
#include <stdio.h>
#include <share.h>

int main() {
    FILE* fLog = _wfsopen(L"test_log.txt", L"a, ccs=UTF-8", _SH_DENYNO);
    if (!fLog) {
        printf("Failed to open file! errno: %d\n", errno);
        return 1;
    }
    fwprintf(fLog, L"Test log entry\n");
    fclose(fLog);
    printf("Success!\n");
    return 0;
}

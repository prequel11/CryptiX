#include <windows.h>
#include <bcrypt.h>
#include <stdint.h>
#include <stddef.h>

// Export this function so that Python can load and call it directly
__declspec(dllexport) int get_os_entropy(unsigned char *buffer, size_t size) {

    // Ask Windows OS to fill buffer with secure random bytes
    NTSTATUS status = BCryptGenRandom(NULL, buffer, (ULONG)size, BCRYPT_USE_SYSTEM_PREFERRED_RNG);

    if (status == 0) {
        return 1;
    }

    return 0;
}
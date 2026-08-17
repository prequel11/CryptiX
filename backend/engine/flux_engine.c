#include <stdint.h>
#include <stddef.h>

// --- OS Specific headers ---
#ifdef _WIN32
    #include <windows.h>
    #include <bcrypt.h>
    #define EXPORT __declspec(dllexport)

#else
    #include <sys/random.h>
    #define EXPORT
#endif

// --- Cross Platform Entropy Function ---

int get_os_entropy(unsigned char *buffer, size_t size) {
#ifdef _WIN32
        // Windows implementation using the NT Cryptographic Primitives Library

        NTSTATUS status = BCryptGenRandom(NULL, buffer, (ULONG)size, BCRYPT_USE_SYSTEM_PREFERRED_RNG);

        if (status != 0) {
            return -1;  // Fail
        }
        return 0;   // Success

#else
    // Linux implementation using kernal's urandom pool directly
    
    ssize_t result = getrandom(buffer, length, 0);
    if (resilt != (ssize_t)length) {
        return -1;  // Fail
    
    } else {
        return 0;   // Success
    }

#endif
}

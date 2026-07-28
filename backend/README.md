# CryptiX: High-Performance Entropy & Key Generation Engine

CryptiX is a high-performance cryptographic key generation and validation system. Designed with a hybrid architecture, it bridges high-level web infrastructure with low-level operating system entropy harvesting through a custom-compiled C Foreign Function Interface (FFI).

## 🚀 Key Features

* **Kernel-Level Entropy Harvesting:** Bypasses standard runtime wrappers to query the Windows NT Cryptographic Primitives Library (`BCryptGenRandom`) directly via a custom C17 shared library.
* **Mathematical Randomness Auditing:** Implements **Shannon Entropy Information Theory ($H(X)$)** to evaluate and prove the density of randomness in real-time ($7.99+$ bits per byte).
* **High-Performance Web API:** Built with **FastAPI** for asynchronous throughput and robust JSON payload validation.
* **State Management & Replay Protection:** Utilizes **SQLite** with atomic constraints to handle key lifecycle states (`unused` -> `used`) and completely prevent collisions or replay attacks.
* **Graceful Degradation:** Features a built-in cryptographic failsafe that drops back to native runtime libraries (`secrets`) if the system kernel call fails.

---

## 🛠️ Architecture

```text
 [ FastAPI Web Server ] 
         │
         ├──► /generate-key ──► [ C17 DLL (BCryptGenRandom) ] ──► Windows Kernel Entropy
         │
         ├──► /audit-system ──► [ Shannon Entropy Math ] ──► Mathematical Grade Proof
         │
         └──► /validate-key ──► [ SQLite Database ] ──► Replay Protection / State Lock
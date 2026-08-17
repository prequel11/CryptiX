from fastapi import FastAPI, HTTPException
from collections import Counter
import ctypes
import textwrap
import secrets
import sqlite3
import math
import sys
import os

app = FastAPI()
DB_FILE = "cryptix.db"

# Initilaize SQLite Database
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS keys (
                key TEXT PRIMARY KEY,
                status TEXT NOT NULL
            )
        """)
init_db()

# Load FLUX ENGINE (C DLL)
flux_engine = None

if sys.platform == "win32":
    binary_name = "flux_engine.dll"

else:
    binary_name = "flux_engine.so"

dll_path = os.path.abspath("engine/flux_engine.dll")

if os.path.exists(dll_path):
    flux_engine = ctypes.CDLL(dll_path)

else:
    print(f"Warning: {binary_name} not found. Using native Python fallback")

# Entropy Generation
def get_secure_entropy(byte_length: int) -> bytes:
    if flux_engine:

        try:
            buffer = ctypes.create_string_buffer(byte_length)
            if flux_engine.get_os_entropy(buffer, byte_length) == 1:
                return buffer.raw

        except Exception as e:
            print("FLUX Engine Error: {e}, Falling back to Python secrets.")
            pass

    return secrets.token_bytes(byte_length)

# Shannon Entropy
def calculate_shannon_entropy(data: bytes) -> float:
    """Calculates the Shannon entropy of a byte sequence (max 8.0)."""

    if not data:
        return 0.0

    entropy = 0.0
    length = len(data)
    occurances = Counter(data)

    for count in occurances.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy

# API Endpoints
@app.get("/")
def home():
    return {"message": "CryptiX Backend Powered by FLUX Engine"}

@app.get("/generate-key")
def generate_key(length: int = 32):
    byte_length = length // 2

    raw_bytes = get_secure_entropy(byte_length)
    secure_hex = raw_bytes.hex()

    # Formatting Key
    formatted_key = "-".join(textwrap.wrap(secure_hex[:length], 4))

    # Thread safe database insertion
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
                "INSERT INTO keys (key, status) VALUES (?, ?)",
                (formatted_key, "unused")
            )

    except sqlite3.IntegrityError:
        raise HTTPException(status_code=500, detail="Key collision detected. Try again")

    return {
        "status": "success",
        "key": formatted_key,
        "engine": "FLUX DLL" if flux_engine else "Python Failsafe"
    }

@app.get("/validate-key")
def validate_key(user_key: str):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("SELECT status FROM keys WHERE key = ?", (user_key,))
        row = cursor.fetchone()

        if not row:
            return {"status": "invalid"}

        if row[0] == "unused":
            conn.execute("UPDATE keys SET status = 'used' WHERE key = ?", (user_key,))
            return {"status": "valid (now marked as used)"}

        else:
            return {"status": "already used"}

@app.get("/audit-system")
def audit_system(test_size_bytes: int = 10000):
    """Pulls a large sample from the FLUX Engine to mathematically prove randomness."""

    # Limit max to prevent memory overload (1MB max)
    if test_size_bytes > 1000000:
        raise HTTPException(status_code=400, detail="Test size too large.")

    raw_bytes = get_secure_entropy(test_size_bytes)
    entropy_score = calculate_shannon_entropy(raw_bytes)

    # Assess quality of randomness
    if entropy_score > 7.99:
        quality = "Cryptographic Grade (Maximum Chaos)"

    elif entropy_score > 7.9:
        quality = "High Quality"

    else:
        quality = "Sub-optimal / Corrupted Entropy Pool"

    return {
        "status": "success",
        "bytes_tested": test_size_bytes,
        "engine": "FLUX DLL" if flux_engine else "Python Failsafe",
        "shannon_entropy": round(entropy_score, 5),
        "theoratical_max": 8.0,
        "quality_assessment": quality
    }
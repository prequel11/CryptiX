from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    """Test API is online."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "CryptiX Backend Powered by FLUX Engine"}

def test_generate_key():
    """Test a key is generated with correct format."""
    response = client.get("/generate-key?length=32")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert "key" in data

    assert len(data["key"].split("-")) == 8

def test_validate_key_lifecycle():
    """Test the full lifecycle: generate a key, validate it, then ensure it can't be reused."""

    # Generate a key
    gen_response = client.get("/generate-key")
    new_key = gen_response.json()["key"]

    # Validate key
    val_response_1 = client.get(f"/validate-key?user_key={new_key}")
    assert val_response_1.status_code == 200
    assert val_response_1.json()["status"] == "valid (now marked as used)"

    # Validating same key again (should be false)
    val_response_2 = client.get(f"/validate-key?user_key={new_key}")
    assert val_response_2.status_code == 200
    assert val_response_2.json()["status"] == "already used"

def test_audit_system():
    """Test Shannon Entropy math engine"""
    response = client.get("/audit-system?test_size_bytes=5000")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert data["bytes_tested"] == 5000
    assert "shannon_entropy" in data
    assert data["shannon_entropy"] > 0.0    # Ensure math is calculating
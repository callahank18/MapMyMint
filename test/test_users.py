from fastapi.testclient import TestClient
from frontend.serverAPI import app
import pytest

client = TestClient(app)

#register user
@pytest.mark.parametrize("username,password,expected_status", [
    ("testuser123", "password123", 409),
    (15, "password123", 422),
    ("testuser123", 21, 422),
    (True, "password123", 422),
    ("testuser123", True, 422),
    (False, "password123", 422),
    ("testuser123", False, 422),
    ("", "password123", 422),
    ("testuser123", "", 422),
    (None, "password123", 422),
    ("testuser123", None, 422),
])
def test_register_user(username, password, expected_status):
    response = client.post("/register/", json={
        "username": username,
        "password": password
    })

    assert response.status_code == expected_status
  




@pytest.mark.parametrize("username,password,expected_status", [
    ("testuser123", "password123", 200),
    ("wronguser", "password123", 401),
    ("testuser123", "wrongpass", 401),
    ("wronguser", "wrongpass", 401),
    (15, "password123", 422),
    ("testuser123", 21, 422),
    (True, "password123", 422),
    ("testuser123", True, 422),
    (False, "password123", 422),
    ("testuser123", False, 422),
    ("", "password123", 422),
    ("testuser123", "", 422),
    (None, "password123", 422),
    ("testuser123", None, 422),
])
def test_login(username, password, expected_status):
    response = client.post("/login/", json={
        "username": username,
        "password": password
    })

    assert response.status_code == expected_status
  
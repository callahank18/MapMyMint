
from fastapi.testclient import TestClient
from frontend.serverAPI import app
import pytest

client = TestClient(app)


# -----------------------------
# FIXTURE: create user
# -----------------------------
@pytest.fixture
def create_user():
    response = client.post("/register/", json={
        "username": "test_user_unique",
        "password": "password123"
    })
    assert response.status_code in [200, 409]  # allow reruns
    if response.status_code == 409:
        response = client.post("/login/", json={
        "username": "test_user_unique",
        "password": "password123"
    })

    return response


# -----------------------------
# FIXTURE: create goal
# -----------------------------
@pytest.fixture
def create_goal(create_user):
    user_id = create_user.json()["user_id"]

    response = client.post("/goals/", json={
        "user_id": user_id,
        "goal_name": "Test Goal",
        "target_amount": 1000,
        "current_amount": 0
    })

    assert response.status_code == 200
    return response.json()["data"] if "data" in response.json() else response.json()


# =====================================================
# GET GOALS TESTS
# =====================================================

def test_get_goals_empty_user():
    user = client.post("/register/", json={
        "username": "empty_user",
        "password": "password123"
    })
    if user.status_code == 200:
        user_id = user.json()["user_id"]
    if user.status_code == 409:
        response = client.post("/login/", json={
        "username": "empty_user",
        "password": "password123"
        })
        user_id = response.json()["user_id"]


    response = client.get(f"/goals/{user_id}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [] or len(response.json()) == 0


def test_get_goals_with_data(create_goal, create_user):
    user_id = create_user.json()["user_id"]

    response = client.get(f"/goals/{user_id}")

    assert response.status_code == 200

    data = response.json()

    # API currently returns list directly
    assert isinstance(data, list)
    assert len(data) >= 1

    assert "goal_id" in data[0]
    assert "goal_name" in data[0]


def test_get_goals_invalid_user():
    response = client.get("/goals/99999999")

    assert response.status_code == 404


def test_get_goals_invalid_type():
    response = client.get("/goals/abc")

    assert response.status_code == 422


# =====================================================
# UPDATE GOAL TESTS
# =====================================================

def test_update_goal_success(create_goal):
    goal_id = create_goal["goal_id"]

    response = client.put(f"/goals/{goal_id}", json={
        "current_amount": 500
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_update_goal_not_found():
    response = client.put("/goals/999999", json={
        "current_amount": 500
    })

    assert response.status_code == 400


def test_update_goal_invalid_payload(create_goal):
    goal_id = create_goal["goal_id"]

    response = client.put(f"/goals/{goal_id}", json={
        "current_amount": "bad_value"
    })

    assert response.status_code == 422


def test_update_goal_missing_field(create_goal):
    goal_id = create_goal["goal_id"]

    response = client.put(f"/goals/{goal_id}", json={})

    assert response.status_code == 422
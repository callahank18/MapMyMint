
from fastapi.testclient import TestClient
from frontend.serverAPI import app
import pytest

client = TestClient(app)



@pytest.mark.parametrize("user_id, goal_name, target_amount, current_amount, expected_status", [
    (1,"Test Goal", 100.0, 0.0, 200),
    (1,"", 100.0, 0.0, 422),
    (None,"Test Goal", 100.0, 0.0, 422),
    (1,None, 100.0, 0.0, 422),
    (1,"Test Goal", None, 0.0, 422),
    (1,"Test Goal", 100.0, None, 422)
])
def test_create_goal(user_id, goal_name, target_amount, current_amount, expected_status):
    response = client.post("/goals/", json={
        "user_id": user_id,
        "goal_name": goal_name,
        "target_amount": target_amount,
        "current_amount": current_amount
    })

    assert response.status_code == expected_status

    #cleanup whatever was added in the test
    if response.status_code == 200:
        data = response.json()
        goal_data = data["data"]
        goal_id = goal_data["goal_id"]

        from backend.models import SessionLocal, Goals
        db = SessionLocal()
        db.query(Goals).filter(Goals.goal_id == goal_id).delete()
        db.commit()
        db.close()



@pytest.mark.parametrize("user_id, expected_status", [
    (1, 200),   #200=ok uid is taken
    (999999, 404), #404=not found because the uid id not taken
    ("", 405),  #405=no route because there is no input
    ("UID", 422)
])
def test_get_goal(user_id, expected_status):
    response = client.get(f"/goals/{user_id}")
    assert response.status_code == expected_status


@pytest.mark.parametrize("goal_id, payload, expected_status", [
    (1, {"current_amount": 100}, 200),
    (9999, {"current_amount": 100}, 400),
    (1, {"current_amount": "bad"}, 422),
    (1, {}, 422),
])
def test_update_goal(goal_id, payload, expected_status):

    old_value = None

    # Only try to get original if we expect success
    if expected_status == 200:
        original = client.get(f"/goals/{goal_id}").json()

        # If your API wraps response in "data"
        if isinstance(original, dict) and "data" in original:
            original = original["data"]

        goal = next(g for g in original if g["goal_id"] == goal_id)
        old_value = goal["current_amount"]

    # Perform update
    response = client.put(f"/goals/{goal_id}", json=payload)
    assert response.status_code == expected_status

    if expected_status != 200:
        return

    # Verify update
    updated = client.get(f"/goals/{goal_id}").json()

    if isinstance(updated, dict) and "data" in updated:
        updated = updated["data"]

    goal = next(g for g in updated if g["goal_id"] == goal_id)
    assert goal["current_amount"] == payload["current_amount"]

    # Restore original value
    client.put(
        f"/goals/{goal_id}",
        json={"current_amount": old_value}
    )
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure clean state by attempting to unregister first
    client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Signup
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert email in res.json().get("message", "")

    # Verify participant added
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    assert email in participants

    # Unregister
    res = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert res.status_code == 200
    assert email in res.json().get("message", "")

    # Verify participant removed
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    assert email not in participants


def test_signup_existing_fails():
    activity = "Chess Club"
    existing = "michael@mergington.edu"
    res = client.post(f"/activities/{activity}/signup", params={"email": existing})
    assert res.status_code == 400

import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

ACTIVITY = "Chess Club"
EMAIL = "testuser@mergington.edu"


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert ACTIVITY in data
    assert "participants" in data[ACTIVITY]


def test_signup_for_activity():
    # Remove if already present
    client.delete(f"/activities/{ACTIVITY}/unregister", params={"email": EMAIL})
    response = client.post(f"/activities/{ACTIVITY}/signup", params={"email": EMAIL})
    assert response.status_code == 200
    assert f"Signed up {EMAIL}" in response.json()["message"]
    # Check participant added
    activities = client.get("/activities").json()
    assert EMAIL in activities[ACTIVITY]["participants"]


def test_prevent_duplicate_signup():
    response = client.post(f"/activities/{ACTIVITY}/signup", params={"email": EMAIL})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_from_activity():
    response = client.delete(f"/activities/{ACTIVITY}/unregister", params={"email": EMAIL})
    assert response.status_code == 200
    assert f"Unregistered {EMAIL}" in response.json()["message"]
    # Check participant removed
    activities = client.get("/activities").json()
    assert EMAIL not in activities[ACTIVITY]["participants"]


def test_unregister_nonexistent():
    response = client.delete(f"/activities/{ACTIVITY}/unregister", params={"email": EMAIL})
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

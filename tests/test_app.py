import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from app import app

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_unregister():
    activity = "Basketball"
    email = "testuser@example.com"

    # Ensure email not present
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Sign up
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # Confirm presence
    res = client.get("/activities")
    assert email in res.json()[activity]["participants"]

    # Unregister
    res = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert res.status_code == 200
    assert "Unregistered" in res.json().get("message", "")

    # Confirm removal
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]

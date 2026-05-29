import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Remove if already present
    client.delete(f"/activities/{activity}/remove", params={"email": email})
    # Signup
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response_dup.status_code == 400
    # Remove
    response_rm = client.delete(f"/activities/{activity}/remove", params={"email": email})
    assert response_rm.status_code == 200
    assert f"Removed {email}" in response_rm.json()["message"]
    # Remove again (should fail)
    response_rm2 = client.delete(f"/activities/{activity}/remove", params={"email": email})
    assert response_rm2.status_code == 404

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404

def test_remove_invalid_activity():
    response = client.delete("/activities/Nonexistent/remove", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404

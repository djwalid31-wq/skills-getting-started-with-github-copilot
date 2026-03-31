import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# --- GET /activities ---
def test_get_activities():
    # Arrange: rien à préparer, état initial
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# --- POST /activities/{activity_name}/signup ---
def test_signup_for_activity():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert f"Signed up {email}" in data["message"]
    # Clean up: remove test user
    client.post(f"/activities/{activity}/unregister?email={email}")

# --- POST /activities/{activity_name}/unregister ---
def test_unregister_from_activity():
    # Arrange
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    # S'inscrire d'abord
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert f"Removed {email}" in data["message"]

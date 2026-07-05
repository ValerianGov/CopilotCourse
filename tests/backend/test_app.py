from fastapi.testclient import TestClient

from src.app import activities, app


def test_duplicate_signup_returns_conflict():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    original_participants = list(activities[activity_name]["participants"])
    email = original_participants[0]

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 409
        assert response.json()["detail"] == "Student already signed up"
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_email():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    original_participants = list(activities[activity_name]["participants"])
    email = original_participants[0]

    try:
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_successful_signup_adds_participant():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    original_participants = list(activities[activity_name]["participants"])
    email = "new.student@mergington.edu"

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants

from fastapi.testclient import TestClient

from src.app import activities, app


def test_duplicate_signup_returns_conflict():
    client = TestClient(app)
    activity_name = "Chess Club"
    original_participants = list(activities[activity_name]["participants"])

    try:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": original_participants[0]},
        )

        assert response.status_code == 409
        assert response.json()["detail"] == "Student already signed up"
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_email():
    client = TestClient(app)
    activity_name = "Chess Club"
    original_participants = list(activities[activity_name]["participants"])

    try:
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": original_participants[0]},
        )

        assert response.status_code == 200
        assert original_participants[0] not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants

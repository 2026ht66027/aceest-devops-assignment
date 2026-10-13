import pytest

from app import create_app


@pytest.fixture
def client():
    return create_app({"TESTING": True, "SECRET_KEY": "test-secret"}).test_client()

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"ACEest Fitness" in response.data

def test_health_endpoint(client):
    assert client.get("/health").get_json() == {"status": "ok"}

def test_add_workout(client):
    response = client.post("/workouts", data={"name": "Walking", "duration": "30"}, follow_redirects=True)
    assert b"Walking" in response.data and b"30 minutes" in response.data

def test_blank_name_rejected(client):
    response = client.post("/workouts", data={"name": " ", "duration": "30"}, follow_redirects=True)
    assert b"Workout name is required." in response.data

@pytest.mark.parametrize("duration", ["0", "-1", "abc", "1441", ""])
def test_invalid_duration_rejected(client, duration):
    response = client.post("/workouts", data={"name": "Walking", "duration": duration}, follow_redirects=True)
    assert b"Duration must be between 1 and 1440 minutes." in response.data
    assert b"Walking" not in response.data

def test_delete_workout(client):
    client.post("/workouts", data={"name": "Cycling", "duration": "45"})
    response = client.post("/workouts/1/delete", follow_redirects=True)
    assert b"Cycling" not in response.data and b"Workout deleted." in response.data

def test_intentional_failure_for_rollback_demo():
    """Temporary test to demonstrate CI failure handling."""
    assert 1 == 2, "Intentional failure for rollback demonstration"

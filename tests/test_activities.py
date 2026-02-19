import urllib.parse
from copy import deepcopy

import src.app as app_module


def test_get_activities(client):
    # Arrange
    expected = deepcopy(app_module.activities)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    assert resp.json() == expected


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    url = f"/activities/{urllib.parse.quote(activity)}/signup"

    # Act
    resp = client.post(url, params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert resp.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in app_module.activities[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already signed up in the initial data
    url = f"/activities/{urllib.parse.quote(activity)}/signup"

    # Act
    resp = client.post(url, params={"email": email})

    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "someone@mergington.edu"
    url = f"/activities/{urllib.parse.quote(activity)}/signup"

    # Act
    resp = client.post(url, params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"


def test_remove_participant_success(client):
    # Arrange
    activity = "Basketball Team"
    email = "james@mergington.edu"  # present in initial participants
    url = f"/activities/{urllib.parse.quote(activity)}/participants"

    # Act
    resp = client.delete(url, params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert resp.json() == {"message": f"Removed {email} from {activity}"}
    assert email not in app_module.activities[activity]["participants"]


def test_remove_nonexistent_participant(client):
    # Arrange
    activity = "Basketball Team"
    email = "not-in-list@mergington.edu"
    url = f"/activities/{urllib.parse.quote(activity)}/participants"

    # Act
    resp = client.delete(url, params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found in this activity"


def test_root_redirect(client):
    # Arrange

    # Act
    resp = client.get("/", follow_redirects=False)

    # Assert
    assert resp.status_code in (301, 302, 307, 308)
    assert resp.headers.get("location") == "/static/index.html"

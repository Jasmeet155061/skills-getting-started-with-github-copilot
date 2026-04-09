"""
Integration tests for FastAPI endpoints using the AAA (Arrange-Act-Assert) pattern.

Tests cover:
- GET /activities: List all activities
- GET /: Redirect to static files
- POST /activities/{activity_name}/signup: Student signup (happy path and error cases)
- DELETE /activities/{activity_name}/unregister: Student unregistration (happy path and error cases)
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns a dictionary of all available activities.
        
        Arrange: No special setup needed
        Act: Make GET request to /activities
        Assert: Response status is 200 and returns dict of activities with required fields
        """
        # Arrange (no setup needed)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        
        # Verify each activity has required fields
        for activity_name, activity in data.items():
            assert isinstance(activity_name, str)
            assert "description" in activity
            assert "schedule" in activity
            assert "participants" in activity
            assert "max_participants" in activity
            assert isinstance(activity["participants"], list)


class TestRedirect:
    """Tests for GET / endpoint."""

    def test_redirect_to_static_index(self, client):
        """
        Test that GET / redirects to the static index.html file.
        
        Arrange: No special setup needed
        Act: Make GET request to / with follow_redirects=False
        Assert: Response is redirect (307) to /static/index.html
        """
        # Arrange (no setup needed)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert "location" in response.headers
        assert response.headers["location"] == "/static/index.html"


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_student_signup_success(self, client):
        """
        Test that a student can successfully sign up for an activity.
        
        Arrange: Prepare activity name and email
        Act: Make POST request to signup endpoint
        Assert: Status 200 and response confirms signup
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "student@example.com"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_student_signup_duplicate_email_fails(self, client):
        """
        Test that signing up the same student twice returns an error.
        
        Arrange: Student signs up once
        Act: Attempt to sign up the same student again
        Assert: Status 400 (bad request) for duplicate signup
        """
        # Arrange
        activity_name = "Chess Club"
        email = "student@example.com"
        
        # First signup should succeed
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act: Attempt duplicate signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400

    def test_student_signup_nonexistent_activity_fails(self, client):
        """
        Test that signing up for a non-existent activity returns an error.
        
        Arrange: Prepare a non-existent activity name and email
        Act: Make POST request with non-existent activity
        Assert: Status 404 (not found)
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@example.com"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_student_unregister_success(self, client):
        """
        Test that a student can successfully unregister from an activity.
        
        Arrange: Student signs up for an activity
        Act: Make DELETE request to unregister
        Assert: Status 200 and response confirms unregistration
        """
        # Arrange
        activity_name = "Chess Club"
        email = "student@example.com"
        
        # Sign up first
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_student_unregister_not_registered_fails(self, client):
        """
        Test that unregistering a student who isn't registered returns an error.
        
        Arrange: Prepare activity name and email of student not registered
        Act: Make DELETE request for unregistered student
        Assert: Status 400 (bad request)
        """
        # Arrange
        activity_name = "Chess Club"
        email = "not_registered@example.com"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400

    def test_student_unregister_nonexistent_activity_fails(self, client):
        """
        Test that unregistering from a non-existent activity returns an error.
        
        Arrange: Prepare a non-existent activity name and email
        Act: Make DELETE request with non-existent activity
        Assert: Status 404 (not found)
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@example.com"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404

"""
Tests for the GET /activities endpoint.

Uses the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test fixtures and data
- Act: Perform the HTTP request
- Assert: Verify the response status, structure, and content
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, activity_names):
        """
        AAA Test: Get activities endpoint returns all 9 activities with correct count.
        
        Arrange: Initialize TestClient (via fixture)
        Act: Send GET request to /activities
        Assert: Verify status 200 and all activities are returned
        """
        # Arrange
        expected_count = len(activity_names)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_count
        assert all(name in activities for name in activity_names)

    def test_get_activities_returns_correct_structure(self, client, valid_activity_name):
        """
        AAA Test: Each activity in response has required fields.
        
        Arrange: Initialize TestClient (via fixture)
        Act: Send GET request to /activities
        Assert: Verify each activity has required fields: description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        activity = activities[valid_activity_name]
        assert all(field in activity for field in required_fields)

    def test_get_activities_response_is_dict(self, client):
        """
        AAA Test: Response is a dictionary (not a list or other type).
        
        Arrange: Initialize TestClient (via fixture)
        Act: Send GET request to /activities
        Assert: Verify response is a dictionary
        """
        # Arrange
        # (setup via fixture)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)

    def test_get_activities_participants_is_list(self, client, valid_activity_name):
        """
        AAA Test: Each activity's participants field is a list.
        
        Arrange: Initialize TestClient (via fixture)
        Act: Send GET request to /activities
        Assert: Verify participants field is a list for each activity
        """
        # Arrange
        # (setup via fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        activity = activities[valid_activity_name]
        assert isinstance(activity["participants"], list)

    def test_get_activities_has_initial_participants(self, client, valid_activity_name):
        """
        AAA Test: Activities have pre-populated participants from initial data.
        
        Arrange: Initialize TestClient (via fixture)
        Act: Send GET request to /activities
        Assert: Verify at least one activity has participants
        """
        # Arrange
        # (setup via fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        activity = activities[valid_activity_name]
        assert len(activity["participants"]) > 0

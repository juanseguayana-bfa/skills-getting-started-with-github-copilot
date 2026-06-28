"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint.

Uses the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test fixtures and data
- Act: Perform the HTTP request
- Assert: Verify the response status, structure, and content
"""

import pytest


class TestRemoveParticipant:
    """Test suite for DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_remove_participant_succeeds(self, client, valid_activity_name, valid_email):
        """
        AAA Test: Remove a participant from an activity returns 200 and success message.
        
        Arrange: Sign up a participant, then prepare to remove them
        Act: Send DELETE request to remove endpoint
        Assert: Verify status 200 and success message in response
        """
        # Arrange
        signup_url = f"/activities/{valid_activity_name}/signup"
        client.post(signup_url, params={"email": valid_email})
        delete_url = f"/activities/{valid_activity_name}/participants/{valid_email}"

        # Act
        response = client.delete(delete_url)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert valid_email in data["message"]
        assert valid_activity_name in data["message"]

    def test_remove_participant_removes_from_list(self, client, valid_activity_name, valid_email):
        """
        AAA Test: After removal, participant is no longer in activity's participant list.
        
        Arrange: Sign up a participant, then remove them
        Act: Get activities to verify removal
        Assert: Verify participant is no longer in the list
        """
        # Arrange
        signup_url = f"/activities/{valid_activity_name}/signup"
        delete_url = f"/activities/{valid_activity_name}/participants/{valid_email}"
        client.post(signup_url, params={"email": valid_email})

        # Act
        client.delete(delete_url)
        response = client.get("/activities")
        activities = response.json()

        # Assert
        participants = activities[valid_activity_name]["participants"]
        assert valid_email not in participants

    def test_remove_nonexistent_activity_returns_404(self, client, invalid_activity_name, valid_email):
        """
        AAA Test: Removal from nonexistent activity returns 404 error.
        
        Arrange: Prepare invalid activity name and valid email
        Act: Send DELETE request with nonexistent activity
        Assert: Verify status 404 and error detail
        """
        # Arrange
        delete_url = f"/activities/{invalid_activity_name}/participants/{valid_email}"

        # Act
        response = client.delete(delete_url)

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_unregistered_participant_returns_404(self, client, valid_activity_name, valid_email):
        """
        AAA Test: Removal of unregistered participant returns 404 error.
        
        Arrange: Prepare valid activity and email (without signing up)
        Act: Send DELETE request for email not in participant list
        Assert: Verify status 404 and error message about not signed up
        """
        # Arrange
        delete_url = f"/activities/{valid_activity_name}/participants/{valid_email}"

        # Act
        response = client.delete(delete_url)

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_remove_multiple_participants_individually(self, client, valid_activity_name, valid_email, another_valid_email):
        """
        AAA Test: Can remove multiple participants individually from the same activity.
        
        Arrange: Sign up two participants
        Act: Remove them one at a time
        Assert: Verify both are removed correctly
        """
        # Arrange
        signup_url = f"/activities/{valid_activity_name}/signup"
        client.post(signup_url, params={"email": valid_email})
        client.post(signup_url, params={"email": another_valid_email})

        # Act
        response1 = client.delete(f"/activities/{valid_activity_name}/participants/{valid_email}")
        response2 = client.delete(f"/activities/{valid_activity_name}/participants/{another_valid_email}")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        response = client.get("/activities")
        activities = response.json()
        participants = activities[valid_activity_name]["participants"]
        assert valid_email not in participants
        assert another_valid_email not in participants

    def test_remove_same_participant_twice_returns_404(self, client, valid_activity_name, valid_email):
        """
        AAA Test: Removing a participant twice returns 404 on second attempt.
        
        Arrange: Sign up a participant and remove them once
        Act: Attempt to remove the same participant again
        Assert: Verify status 404 on second removal
        """
        # Arrange
        signup_url = f"/activities/{valid_activity_name}/signup"
        delete_url = f"/activities/{valid_activity_name}/participants/{valid_email}"
        client.post(signup_url, params={"email": valid_email})
        client.delete(delete_url)

        # Act
        response = client.delete(delete_url)

        # Assert
        assert response.status_code == 404

    def test_remove_response_format(self, client, valid_activity_name, valid_email):
        """
        AAA Test: Remove response has correct format with message field.
        
        Arrange: Sign up a participant
        Act: Remove the participant
        Assert: Verify response JSON has required structure
        """
        # Arrange
        signup_url = f"/activities/{valid_activity_name}/signup"
        delete_url = f"/activities/{valid_activity_name}/participants/{valid_email}"
        client.post(signup_url, params={"email": valid_email})

        # Act
        response = client.delete(delete_url)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)

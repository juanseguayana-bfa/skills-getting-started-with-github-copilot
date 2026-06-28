"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Uses the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test fixtures and data
- Act: Perform the HTTP request
- Assert: Verify the response status, structure, and content
"""

import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_with_valid_data_succeeds(self, client, valid_activity_name, valid_email):
        """
        AAA Test: Signup with valid activity and email returns 200 and success message.
        
        Arrange: Prepare valid activity name and email
        Act: Send POST request to signup endpoint
        Assert: Verify status 200 and success message in response
        """
        # Arrange
        url = f"/activities/{valid_activity_name}/signup"
        params = {"email": valid_email}

        # Act
        response = client.post(url, params=params)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert valid_email in data["message"]
        assert valid_activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client, valid_activity_name, valid_email):
        """
        AAA Test: After signup, participant appears in activity's participant list.
        
        Arrange: Prepare valid activity and email, then signup
        Act: Send GET request to verify participant was added
        Assert: Verify participant is in the participants list
        """
        # Arrange
        signup_url = f"/activities/{valid_activity_name}/signup"
        signup_params = {"email": valid_email}
        client.post(signup_url, params=signup_params)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        participants = activities[valid_activity_name]["participants"]
        assert valid_email in participants

    def test_signup_multiple_participants(self, client, valid_activity_name, valid_email, another_valid_email):
        """
        AAA Test: Multiple participants can signup to the same activity.
        
        Arrange: Prepare two valid emails and activity
        Act: Sign up both participants
        Assert: Verify both are in the participants list
        """
        # Arrange
        signup_url = f"/activities/{valid_activity_name}/signup"

        # Act
        response1 = client.post(signup_url, params={"email": valid_email})
        response2 = client.post(signup_url, params={"email": another_valid_email})

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        response = client.get("/activities")
        activities = response.json()
        participants = activities[valid_activity_name]["participants"]
        assert valid_email in participants
        assert another_valid_email in participants

    def test_signup_with_nonexistent_activity_returns_404(self, client, invalid_activity_name, valid_email):
        """
        AAA Test: Signup for nonexistent activity returns 404 error.
        
        Arrange: Prepare invalid activity name and valid email
        Act: Send POST request with nonexistent activity
        Assert: Verify status 404 and error detail in response
        """
        # Arrange
        url = f"/activities/{invalid_activity_name}/signup"
        params = {"email": valid_email}

        # Act
        response = client.post(url, params=params)

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_duplicate_returns_400(self, client, valid_activity_name, valid_email):
        """
        AAA Test: Duplicate signup (same email to same activity) returns 400 error.
        
        Arrange: Sign up a participant once
        Act: Attempt to sign up the same participant again
        Assert: Verify status 400 and error message about already signed up
        """
        # Arrange
        url = f"/activities/{valid_activity_name}/signup"
        params = {"email": valid_email}
        client.post(url, params=params)

        # Act
        response = client.post(url, params=params)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_missing_email_parameter_returns_422(self, client, valid_activity_name):
        """
        AAA Test: Signup without email parameter returns 422 validation error.
        
        Arrange: Prepare request without email parameter
        Act: Send POST request without required email
        Assert: Verify status 422 (unprocessable entity)
        """
        # Arrange
        url = f"/activities/{valid_activity_name}/signup"

        # Act
        response = client.post(url)

        # Assert
        assert response.status_code == 422

    def test_signup_response_format(self, client, valid_activity_name, valid_email):
        """
        AAA Test: Signup response has correct format with message field.
        
        Arrange: Prepare valid signup data
        Act: Send POST request
        Assert: Verify response JSON has required structure
        """
        # Arrange
        url = f"/activities/{valid_activity_name}/signup"
        params = {"email": valid_email}

        # Act
        response = client.post(url, params=params)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)

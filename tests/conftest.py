"""
Shared test fixtures and configuration for FastAPI tests.

This module provides fixtures for test setup, including TestClient initialization
and sample test data (valid and invalid activity names, emails).
"""

import pytest
from fastapi.testclient import TestClient
from src import app as app_module


# Initial activities state for resetting between tests
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for intramural and league play",
        "schedule": "Tuesdays, Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["marcus@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn and practice tennis skills with coaching",
        "schedule": "Wednesdays, Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu", "jessica@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and mixed media techniques",
        "schedule": "Mondays, Wednesdays, 3:45 PM - 5:15 PM",
        "max_participants": 18,
        "participants": ["sarah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in theatrical productions and develop acting skills",
        "schedule": "Thursdays, Fridays, 4:00 PM - 5:45 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "anna@mergington.edu", "noah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills through competitive debate",
        "schedule": "Tuesdays, Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["grace@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore advanced scientific concepts",
        "schedule": "Mondays, Fridays, 3:30 PM - 4:45 PM",
        "max_participants": 22,
        "participants": ["andrew@mergington.edu", "sophie@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for the FastAPI app.
    
    Reset the in-memory activities database before each test to ensure proper
    test isolation and prevent state leakage between tests.
    """
    # Clear existing activities and repopulate (instead of replacing the dict reference)
    app_module.activities.clear()
    
    for key, value in INITIAL_ACTIVITIES.items():
        app_module.activities[key] = {
            "description": value["description"],
            "schedule": value["schedule"],
            "max_participants": value["max_participants"],
            "participants": value["participants"].copy()  # Copy the list
        }
    
    return TestClient(app_module.app)


@pytest.fixture
def valid_activity_name():
    """Fixture providing a valid activity name that exists in the app."""
    return "Chess Club"


@pytest.fixture
def valid_email():
    """Fixture providing a valid email for test signup operations."""
    return "testuser@mergington.edu"


@pytest.fixture
def another_valid_email():
    """Fixture providing another valid email for multiple signup tests."""
    return "anotheruser@mergington.edu"


@pytest.fixture
def activity_names():
    """Fixture providing all valid activity names in the system."""
    return [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Drama Club",
        "Debate Team",
        "Science Club"
    ]


@pytest.fixture
def invalid_activity_name():
    """Fixture providing an activity name that does not exist."""
    return "Nonexistent Activity"


@pytest.fixture
def invalid_email():
    """Fixture providing an invalid email format."""
    return "not-an-email"

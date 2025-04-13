"""
Tests for course endpoints.
"""

import pytest
from fastapi.testclient import TestClient

def test_get_courses(test_client: TestClient, auth_headers):
    """
    Test getting all courses.
    """
    response = test_client.get(
        "/api/v1/courses/",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    if data:
        course = data[0]
        assert "id" in course
        assert "title" in course
        assert "description" in course
        assert "instructor_id" in course

def test_get_course_by_id(test_client: TestClient, auth_headers):
    """
    Test getting a course by ID.
    """
    # First, get all courses to find a valid ID
    response = test_client.get(
        "/api/v1/courses/",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    courses = response.json()
    
    if not courses:
        pytest.skip("No courses available for testing")
    
    course_id = courses[0]["id"]
    
    # Now get the specific course
    response = test_client.get(
        f"/api/v1/courses/{course_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    course = response.json()
    assert course["id"] == course_id
    assert "title" in course
    assert "description" in course
    assert "instructor_id" in course

def test_get_nonexistent_course(test_client: TestClient, auth_headers):
    """
    Test getting a course that doesn't exist.
    """
    response = test_client.get(
        "/api/v1/courses/00000000-0000-0000-0000-000000000000",
        headers=auth_headers
    )
    
    assert response.status_code == 404

def test_create_course(test_client: TestClient, auth_headers):
    """
    Test creating a new course.
    """
    # This test assumes the authenticated user has instructor role
    # If not, it will be skipped
    
    # First, check if the user is an instructor
    response = test_client.get(
        "/api/v1/auth/me",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    user = response.json()
    
    if user["role"] != "instructor" and user["role"] != "admin":
        pytest.skip("Test user is not an instructor or admin")
    
    # Create a new course
    response = test_client.post(
        "/api/v1/courses/",
        headers=auth_headers,
        json={
            "title": "Test Course",
            "description": "This is a test course created by automated tests.",
            "status": "draft"
        }
    )
    
    assert response.status_code == 200
    course = response.json()
    assert course["title"] == "Test Course"
    assert course["description"] == "This is a test course created by automated tests."
    assert course["status"] == "draft"
    assert "id" in course

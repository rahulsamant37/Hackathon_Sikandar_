"""
Tests for AI-related endpoints.
"""

import pytest
from fastapi.testclient import TestClient

def test_get_recommendations(test_client: TestClient, auth_headers):
    """
    Test getting personalized recommendations.
    """
    response = test_client.get(
        "/api/v1/ai/recommendations",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)
    
    if recommendations:
        recommendation = recommendations[0]
        assert "id" in recommendation
        assert "user_id" in recommendation
        assert "content_id" in recommendation
        assert "recommendation_type" in recommendation
        assert "reasoning" in recommendation

def test_analyze_learning_style(test_client: TestClient, auth_headers):
    """
    Test analyzing learning style.
    """
    response = test_client.post(
        "/api/v1/ai/analyze-learning-style",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "status" in result
    assert result["status"] == "analysis_started"

def test_get_learning_path(test_client: TestClient, auth_headers):
    """
    Test getting a personalized learning path.
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
    
    # Now get the learning path for this course
    response = test_client.get(
        f"/api/v1/learning-paths/{course_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    learning_path = response.json()
    assert "recommended_sequence" in learning_path
    assert isinstance(learning_path["recommended_sequence"], list)
    assert "focus_areas" in learning_path
    assert "estimated_completion_time" in learning_path
    assert "learning_strategy" in learning_path

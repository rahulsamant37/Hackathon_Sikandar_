"""
Tests for authentication endpoints.
"""

import pytest
from fastapi.testclient import TestClient

def test_login(test_client: TestClient):
    """
    Test the login endpoint.
    """
    response = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "student1@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(test_client: TestClient):
    """
    Test login with invalid credentials.
    """
    response = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "invalid@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401

def test_get_current_user(test_client: TestClient, auth_headers):
    """
    Test getting the current user.
    """
    response = test_client.get(
        "/api/v1/auth/me",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "username" in data
    assert "role" in data

def test_get_current_user_no_token(test_client: TestClient):
    """
    Test getting the current user without a token.
    """
    response = test_client.get("/api/v1/auth/me")
    
    assert response.status_code == 401

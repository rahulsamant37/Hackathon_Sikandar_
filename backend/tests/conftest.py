"""
Pytest configuration file for the AI Learning Platform backend tests.
"""

import os
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from supabase import create_client, Client

from app.main import app
from app.core.config import settings

@pytest.fixture(scope="session")
def test_client() -> Generator:
    """
    Create a FastAPI TestClient for testing API endpoints.
    """
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session")
def supabase_client() -> Client:
    """
    Create a Supabase client for testing.
    """
    supabase_url = os.environ.get("TEST_SUPABASE_URL", settings.SUPABASE_URL)
    supabase_key = os.environ.get("TEST_SUPABASE_KEY", settings.SUPABASE_KEY)
    
    if not supabase_url or not supabase_key:
        pytest.skip("Supabase credentials not available for testing")
    
    return create_client(supabase_url, supabase_key)

@pytest.fixture(scope="session")
def test_user_token(supabase_client: Client) -> str:
    """
    Get a JWT token for a test user.
    """
    # Use test credentials
    email = os.environ.get("TEST_USER_EMAIL", "student1@example.com")
    password = os.environ.get("TEST_USER_PASSWORD", "password123")
    
    try:
        response = supabase_client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response.session.access_token
    except Exception as e:
        pytest.skip(f"Could not get test user token: {e}")

@pytest.fixture
def auth_headers(test_user_token: str) -> Dict[str, str]:
    """
    Create authorization headers with JWT token.
    """
    return {"Authorization": f"Bearer {test_user_token}"}

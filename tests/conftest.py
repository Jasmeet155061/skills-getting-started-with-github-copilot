"""
Pytest configuration and shared fixtures for FastAPI integration tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture providing a TestClient instance for testing FastAPI endpoints.
    
    This client allows tests to make HTTP requests to the app
    in a test environment without starting a server.
    """
    return TestClient(app)

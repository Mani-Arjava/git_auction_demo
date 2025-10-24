"""
Tests for main FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to Phobos Backend API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "healthy"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "phobos-backend"


def test_hello_default():
    """Test hello endpoint without name"""
    response = client.get("/hello")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello from Phobos Backend!"
    assert data["name"] == "World"


def test_hello_with_name():
    """Test hello endpoint with name parameter"""
    response = client.get("/hello/Alice")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, Alice!"
    assert data["name"] == "Alice"


def test_hello_with_special_characters():
    """Test hello endpoint with special characters"""
    response = client.get("/hello/John%20Doe")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, John Doe!"
    assert data["name"] == "John Doe"


def test_openapi_docs():
    """Test that OpenAPI documentation is available"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "Phobos Backend API"


def test_cors_headers():
    """Test CORS headers are present"""
    response = client.options("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

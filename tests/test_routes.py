"""
Tests for API routes
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHelloEndpoints:
    """Test suite for hello endpoints"""

    def test_hello_empty_name_fails(self):
        """Test that empty name in path returns 404"""
        # FastAPI will return 404 for empty path segments
        response = client.get("/hello/")
        assert response.status_code in [404, 307]  # 307 redirect or 404

    def test_hello_long_name(self):
        """Test hello endpoint with long name"""
        long_name = "A" * 100
        response = client.get(f"/hello/{long_name}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == long_name

    def test_hello_unicode_name(self):
        """Test hello endpoint with unicode characters"""
        response = client.get("/hello/世界")
        assert response.status_code == 200
        data = response.json()
        assert "世界" in data["message"]

    def test_hello_numeric_name(self):
        """Test hello endpoint with numeric name"""
        response = client.get("/hello/12345")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "12345"


class TestResponseModels:
    """Test response models and validation"""

    def test_hello_response_structure(self):
        """Test that hello response has correct structure"""
        response = client.get("/hello/Test")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "name" in data
        assert isinstance(data["message"], str)
        assert isinstance(data["name"], str)

    def test_root_response_structure(self):
        """Test that root response has correct structure"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data


class TestErrorHandling:
    """Test error handling"""

    def test_not_found_route(self):
        """Test that non-existent routes return 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_invalid_method(self):
        """Test that invalid HTTP methods are handled"""
        response = client.post("/hello")
        assert response.status_code == 405  # Method not allowed

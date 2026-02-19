#!/usr/bin/python3
"""
Unit tests for Amenity endpoints and models
"""
import pytest
from app import create_app
from app.models.amenity import Amenity

@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture
def sample_amenity_data():
    """Sample amenity data for testing"""
    return {
        "name": "WiFi",
        "description": "High-speed internet connection"
    }

@pytest.fixture
def created_amenity(client, sample_amenity_data):
    """Create an amenity and return its ID"""
    response = client.post("/api/v1/amenities/", json=sample_amenity_data)
    return response.get_json()["id"]

# ========== CREATE AMENITY TESTS ==========

def test_create_amenity_success(client, sample_amenity_data):
    """Test successful amenity creation"""
    response = client.post("/api/v1/amenities/", json=sample_amenity_data)
    
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == sample_amenity_data["name"]
    assert data["description"] == sample_amenity_data["description"]

def test_create_amenity_minimal(client):
    """Test creating amenity with only name"""
    amenity_data = {
        "name": "Pool"
    }
    response = client.post("/api/v1/amenities/",

#!/usr/bin/python3
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_create_amenity_success(client):
    data = {"name": "WiFi", "description": "High-speed internet"}
    res = client.post("/api/v1/amenities/", json=data)
    assert res.status_code == 201
    result = res.get_json()
    assert result["name"] == "WiFi"

def test_create_amenity_missing_name(client):
    res = client.post("/api/v1/amenities/", json={"description": "No name"})
    assert res.status_code == 400
    assert "error" in res.get_json()

def test_get_all_amenities(client):
    res = client.get("/api/v1/amenities/")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

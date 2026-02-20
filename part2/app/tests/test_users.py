#!/usr/bin/python3
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_create_user_success(client):
    user_data = {"email": "john@example.com", "first_name": "John", "last_name": "Doe", "password": "1234"}
    res = client.post("/api/v1/users/", json=user_data)
    assert res.status_code == 201
    data = res.get_json()
    assert data["email"] == "john@example.com"

def test_create_user_missing_email(client):
    user_data = {"first_name": "Jane", "last_name": "Doe"}
    res = client.post("/api/v1/users/", json=user_data)
    assert res.status_code == 400
    assert "error" in res.get_json()

def test_get_user_by_id(client):
    user_data = {"email": "get@example.com", "first_name": "Get", "last_name": "User", "password": "1234"}
    res = client.post("/api/v1/users/", json=user_data)
    user_id = res.get_json()["id"]
    res2 = client.get(f"/api/v1/users/{user_id}")
    assert res2.status_code == 200
    assert res2.get_json()["id"] == user_id

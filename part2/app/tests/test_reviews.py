#!/usr/bin/python3
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture
def test_user(client):
    data = {"email": "reviewer@test.com", "first_name": "Rev", "last_name": "User", "password": "1234"}
    res = client.post("/api/v1/users/", json=data)
    return res.get_json()

@pytest.fixture
def test_place(client, test_user):
    data = {
        "title": "Test Place",
        "price": 100,
        "latitude": 0,
        "longitude": 0,
        "owner_id": test_user["id"]
    }
    res = client.post("/api/v1/places/", json=data)
    return res.get_json()

def test_create_review_success(client, test_user, test_place):
    data = {"text": "Great!", "rating": 5, "user_id": test_user["id"], "place_id": test_place["id"]}
    res = client.post("/api/v1/reviews/", json=data)
    assert res.status_code == 201
    r = res.get_json()
    assert r["text"] == "Great!"
    assert r["rating"] == 5

def test_create_review_missing_text(client, test_user, test_place):
    data = {"rating": 4, "user_id": test_user["id"], "place_id": test_place["id"]}
    res = client.post("/api/v1/reviews/", json=data)
    assert res.status_code == 400
    assert "error" in res.get_json()

def test_get_reviews_by_place(client, test_user, test_place):
    data = {"text": "Nice", "rating": 4, "user_id": test_user["id"], "place_id": test_place["id"]}
    client.post("/api/v1/reviews/", json=data)
    res = client.get(f"/api/v1/places/{test_place['id']}/reviews/")
    assert res.status_code == 200
    assert len(res.get_json()) >= 1

#!/usr/bin/python3
"""
Unit tests for Place endpoints and models (updated for HBnBFacade)
"""
import pytest
from app import create_app
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review

@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture
def test_user(client):
    """Create a test user and return its data"""
    user_data = {
        "email": "owner@test.com",
        "password": "1234",
        "first_name": "Owner",
        "last_name": "Test"
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response.get_json()

@pytest.fixture
def sample_place_data(test_user):
    """Sample place data for testing"""
    return {
        "title": "Beautiful Apartment",
        "price": 100.50,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": test_user["id"]
    }

# ================= CREATE PLACE TESTS =================

def test_create_place_success(client, sample_place_data):
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["title"] == sample_place_data["title"]
    assert data["price"] == sample_place_data["price"]
    assert data["latitude"] == sample_place_data["latitude"]
    assert data["longitude"] == sample_place_data["longitude"]
    assert data["owner_id"] == sample_place_data["owner_id"]

def test_create_place_invalid_owner(client, sample_place_data):
    sample_place_data["owner_id"] = "invalid-owner-id"
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_create_place_missing_title(client, sample_place_data):
    del sample_place_data["title"]
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_empty_title(client, sample_place_data):
    sample_place_data["title"] = ""
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_negative_price(client, sample_place_data):
    sample_place_data["price"] = -50
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_zero_price(client, sample_place_data):
    sample_place_data["price"] = 0
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_invalid_price_format(client, sample_place_data):
    sample_place_data["price"] = "not-a-number"
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

# ================= COORDINATE VALIDATION TESTS =================

def test_create_place_invalid_latitude_high(client, sample_place_data):
    sample_place_data["latitude"] = 100
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400

def test_create_place_invalid_latitude_low(client, sample_place_data):
    sample_place_data["latitude"] = -100
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400

def test_create_place_invalid_longitude_high(client, sample_place_data):
    sample_place_data["longitude"] = 200
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400

def test_create_place_invalid_longitude_low(client, sample_place_data):
    sample_place_data["longitude"] = -200
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400

def test_create_place_valid_coordinate_edges(client, sample_place_data):
    sample_place_data["latitude"] = 90
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 201

    sample_place_data["latitude"] = -90
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 201

    sample_place_data["longitude"] = 180
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 201

    sample_place_data["longitude"] = -180
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 201

# ================= GET PLACE TESTS =================

def test_get_all_places_empty(client):
    response = client.get("/api/v1/places/")
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_all_places_with_data(client, sample_place_data):
    client.post("/api/v1/places/", json=sample_place_data)
    response = client.get("/api/v1/places/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1

def test_get_place_by_id_success(client, sample_place_data):
    create_response = client.post("/api/v1/places/", json=sample_place_data)
    place_id = create_response.get_json()["id"]
    response = client.get(f"/api/v1/places/{place_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == place_id

def test_get_place_invalid_id(client):
    response = client.get("/api/v1/places/invalid-id")
    assert response.status_code == 404
    assert "error" in response.get_json()

# ================= UPDATE PLACE TESTS =================

def test_update_place_success(client, sample_place_data):
    create_response = client.post("/api/v1/places/", json=sample_place_data)
    place_id = create_response.get_json()["id"]
    update_data = {"title": "Updated Title", "price": 200}
    response = client.put(f"/api/v1/places/{place_id}", json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated Title"
    assert data["price"] == 200

def test_update_place_invalid_price(client, sample_place_data):
    create_response = client.post("/api/v1/places/", json=sample_place_data)
    place_id = create_response.get_json()["id"]
    response = client.put(f"/api/v1/places/{place_id}", json={"price": -10})
    assert response.status_code == 400
    assert "error" in response.get_json()

# ================= PLACE MODEL TESTS =================

def test_place_model_creation():
    user = User(email="owner@test.com", first_name="Owner", last_name="Test")
    place = Place(
        title="Test Place",
        price=100,
        latitude=40.7128,
        longitude=-74.0060,
        owner=user
    )
    assert place.title == "Test Place"
    assert place.price == 100.0
    assert place.latitude == 40.7128
    assert place.longitude == -74.0060
    assert place.owner == user
    assert place.amenities == []
    assert place.reviews == []
    assert place.id is not None

def test_place_average_rating_empty():
    user = User(email="owner@test.com", first_name="Owner", last_name="Test")
    place = Place("Test", 100, 0, 0, user)
    assert place.get_average_rating() == 0.0

def test_place_save_method():
    user = User(email="owner@test.com", first_name="Owner", last_name="Test")
    place = Place("Test", 100, 0, 0, user)
    original_updated = place.updated_at
    place.save()
    assert place.updated_at > original_updated

def test_place_add_amenity():
    user = User(email="owner@test.com", first_name="Owner", last_name="Test")
    place = Place("Test", 100, 0, 0, user)
    amenity = Amenity("WiFi")
    place.add_amenity(amenity)
    assert len(place.amenities) == 1
    assert place.amenities[0] == amenity

def test_place_to_dict_with_reviews():
    user = User(email="owner@test.com", first_name="Owner", last_name="Test")
    place = Place("Test", 100, 0, 0, user)
    review1 = Review(5, "Great!", user.id, place.id)
    review2 = Review(4, "Good", user.id, place.id)
    place.add_review(review1)
    place.add_review(review2)
    place_dict = place.to_dict()
    assert "average_rating" in place_dict
    assert place_dict["average_rating"] == 4.5

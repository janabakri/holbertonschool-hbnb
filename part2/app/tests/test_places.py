#!/usr/bin/python3
"""
Unit tests for Place endpoints and models
"""
import pytest
from app import create_app
from app.models.place import Place
from app.models.user import User

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
        "price_per_night": 100.50,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": test_user["id"]
    }

# ========== CREATE PLACE TESTS ==========

def test_create_place_success(client, sample_place_data):
    """Test successful place creation"""
    response = client.post("/api/v1/places/", json=sample_place_data)
    
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["title"] == sample_place_data["title"]
    assert data["price_per_night"] == sample_place_data["price_per_night"]
    assert data["latitude"] == sample_place_data["latitude"]
    assert data["longitude"] == sample_place_data["longitude"]
    assert data["owner_id"] == sample_place_data["owner_id"]

def test_create_place_invalid_owner(client, sample_place_data):
    """Test place creation with invalid owner"""
    sample_place_data["owner_id"] = "invalid-owner-id"
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_create_place_missing_title(client, sample_place_data):
    """Test place creation with missing title"""
    del sample_place_data["title"]
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_empty_title(client, sample_place_data):
    """Test place creation with empty title"""
    sample_place_data["title"] = ""
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_negative_price(client, sample_place_data):
    """Test place creation with negative price"""
    sample_place_data["price_per_night"] = -50
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_zero_price(client, sample_place_data):
    """Test place creation with zero price"""
    sample_place_data["price_per_night"] = 0
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_invalid_price_format(client, sample_place_data):
    """Test place creation with invalid price format"""
    sample_place_data["price_per_night"] = "not-a-number"
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

# ========== COORDINATE VALIDATION TESTS ==========

def test_create_place_invalid_latitude_high(client, sample_place_data):
    """Test place creation with latitude > 90"""
    sample_place_data["latitude"] = 100
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_invalid_latitude_low(client, sample_place_data):
    """Test place creation with latitude < -90"""
    sample_place_data["latitude"] = -100
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_invalid_longitude_high(client, sample_place_data):
    """Test place creation with longitude > 180"""
    sample_place_data["longitude"] = 200
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_invalid_longitude_low(client, sample_place_data):
    """Test place creation with longitude < -180"""
    sample_place_data["longitude"] = -200
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_place_valid_coordinate_edges(client, sample_place_data):
    """Test place creation with edge coordinates"""
    # Test latitude edges
    sample_place_data["latitude"] = 90
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 201
    
    sample_place_data["latitude"] = -90
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 201
    
    # Test longitude edges
    sample_place_data["longitude"] = 180
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 201
    
    sample_place_data["longitude"] = -180
    response = client.post("/api/v1/places/", json=sample_place_data)
    assert response.status_code == 201

# ========== GET PLACES TESTS ==========

def test_get_all_places_empty(client):
    """Test getting all places when none exist"""
    response = client.get("/api/v1/places/")
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_all_places_with_data(client, sample_place_data):
    """Test getting all places after creation"""
    # Create a place
    client.post("/api/v1/places/", json=sample_place_data)
    
    # Get all places
    response = client.get("/api/v1/places/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1

def test_get_place_by_id_success(client, sample_place_data):
    """Test getting place by valid ID"""
    # Create place
    create_response = client.post("/api/v1/places/", json=sample_place_data)
    place_id = create_response.get_json()["id"]
    
    # Get place
    response = client.get(f"/api/v1/places/{place_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == place_id
    assert data["title"] == sample_place_data["title"]

def test_get_place_invalid_id(client):
    """Test getting place with invalid ID"""
    response = client.get("/api/v1/places/invalid-id")
    assert response.status_code == 404
    assert "error" in response.get_json()

# ========== UPDATE PLACE TESTS ==========

def test_update_place_success(client, sample_place_data):
    """Test successful place update"""
    # Create place
    create_response = client.post("/api/v1/places/", json=sample_place_data)
    place_id = create_response.get_json()["id"]
    
    # Update place
    update_data = {
        "title": "Updated Title",
        "price_per_night": 200
    }
    response = client.put(f"/api/v1/places/{place_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated Title"
    assert data["price_per_night"] == 200

def test_update_place_invalid_price(client, sample_place_data):
    """Test updating place with invalid price"""
    # Create place
    create_response = client.post("/api/v1/places/", json=sample_place_data)
    place_id = create_response.get_json()["id"]
    
    # Update with negative price
    response = client.put(f"/api/v1/places/{place_id}", 
                         json={"price_per_night": -10})
    assert response.status_code == 400
    assert "error" in response.get_json()

# ========== PLACE MODEL TESTS ==========

def test_place_model_creation():
    """Test Place model initialization"""
    place = Place(
        title="Test Place",
        price_per_night=100,
        latitude=40.7128,
        longitude=-74.0060,
        owner_id="user-123"
    )
    
    assert place.title == "Test Place"
    assert place.price_per_night == 100.0
    assert place.latitude == 40.7128
    assert place.longitude == -74.0060
    assert place.owner_id == "user-123"
    assert place.amenities == []
    assert place.reviews == []
    assert place.id is not None

def test_place_average_rating_empty():
    """Test average rating with no reviews"""
    place = Place("Test", 100, 0, 0, "owner-123")
    assert place.get_average_rating() == 0.0

def test_place_save_method():
    """Test save method updates timestamp"""
    place = Place("Test", 100, 0, 0, "owner-123")
    original_updated = place.updated_at
    place.save()
    assert place.updated_at > original_updated

def test_place_add_amenity():
    """Test adding amenity to place"""
    from app.models.amenity import Amenity
    
    place = Place("Test", 100, 0, 0, "owner-123")
    amenity = Amenity("WiFi")
    
    place.add_amenity(amenity)
    assert len(place.amenities) == 1
    assert place.amenities[0] == amenity

def test_place_to_dict_with_reviews():
    """Test to_dict includes average rating"""
    from app.models.review import Review
    
    place = Place("Test", 100, 0, 0, "owner-123")
    review1 = Review(5, "Great!", "user-1", "place-1")
    review2 = Review(4, "Good", "user-2", "place-1")
    
    place.add_review(review1)
    place.add_review(review2)
    
    place_dict = place.to_dict()
    assert "average_rating" in place_dict
    assert place_dict["average_rating"] == 4.5

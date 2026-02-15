"""
Unit tests for Review endpoints and models
"""
import pytest
from app import create_app
from app.models.review import Review
from app.models.user import User
from app.models.place import Place

@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture
def test_user(client):
    """Create a test user"""
    user_data = {
        "email": "reviewer@test.com",
        "password": "1234",
        "first_name": "Reviewer",
        "last_name": "Test"
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response.get_json()

@pytest.fixture
def test_owner(client):
    """Create a test owner"""
    owner_data = {
        "email": "owner@test.com",
        "password": "1234",
        "first_name": "Owner",
        "last_name": "Test"
    }
    response = client.post("/api/v1/users/", json=owner_data)
    return response.get_json()

@pytest.fixture
def test_place(client, test_owner):
    """Create a test place"""
    place_data = {
        "title": "Review Place",
        "price_per_night": 100,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": test_owner["id"]
    }
    response = client.post("/api/v1/places/", json=place_data)
    return response.get_json()

@pytest.fixture
def sample_review_data(test_user, test_place):
    """Sample review data for testing"""
    return {
        "rating": 5,
        "comment": "Excellent place! Highly recommended.",
        "user_id": test_user["id"],
        "place_id": test_place["id"]
    }

# ========== CREATE REVIEW TESTS ==========

def test_create_review_success(client, sample_review_data):
    """Test successful review creation"""
    response = client.post("/api/v1/reviews/", json=sample_review_data)
    
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["rating"] == sample_review_data["rating"]
    assert data["comment"] == sample_review_data["comment"]
    assert data["user_id"] == sample_review_data["user_id"]
    assert data["place_id"] == sample_review_data["place_id"]

def test_create_review_invalid_user(client, sample_review_data):
    """Test review creation with invalid user"""
    sample_review_data["user_id"] = "invalid-user-id"
    response = client.post("/api/v1/reviews/", json=sample_review_data)
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_create_review_invalid_place(client, sample_review_data):
    """Test review creation with invalid place"""
    sample_review_data["place_id"] = "invalid-place-id"
    response = client.post("/api/v1/reviews/", json=sample_review_data)
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_create_review_missing_rating(client, sample_review_data):
    """Test review creation with missing rating"""
    del sample_review_data["rating"]
    response = client.post("/api/v1/reviews/", json=sample_review_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_review_missing_comment(client, sample_review_data):
    """Test review creation with missing comment"""
    del sample_review_data["comment"]
    response = client.post("/api/v1/reviews/", json=sample_review_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_review_empty_comment(client, sample_review_data):
    """Test review creation with empty comment"""
    sample_review_data["comment"] = ""
    response = client.post("/api/v1/reviews/", json=sample_review_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

# ========== RATING VALIDATION TESTS ==========

def test_create_review_rating_too_low(client, sample_review_data):
    """Test review creation with rating < 1"""
    sample_review_data["rating"] = 0
    response = client.post("/api/v1/reviews/", json=sample_review_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_review_rating_too_high(client, sample_review_data):
    """Test review creation with rating > 5"""
    sample_review_data["rating"] = 6
    response = client.post("/api/v1/reviews/", json=sample_review_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_review_rating_min_edge(client, sample_review_data):
    """Test review creation with minimum rating (1)"""
    sample_review_data["rating"] = 1
    response = client.post("/api/v1/reviews/", json=sample_review_data)
    assert response.status_code == 201

def test_create_review_rating_max_edge(client, sample_review_data):
    """Test review creation with maximum rating (5)"""
    sample_review_data["rating"] = 5
    response = client.post("/api/v1/reviews/", json=sample_review_data)
    assert response.status_code == 201

def test_create_review_invalid_rating_format(client, sample_review_data):
    """Test review creation with non-integer rating"""
    sample_review_data["rating"] = "five"
    response = client.post("/api/v1/reviews/", json=sample_review_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

# ========== GET REVIEWS TESTS ==========

def test_get_all_reviews_empty(client):
    """Test getting all reviews when none exist"""
    response = client.get("/api/v1/reviews/")
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_all_reviews_with_data(client, sample_review_data):
    """Test getting all reviews after creation"""
    # Create a review
    client.post("/api/v1/reviews/", json=sample_review_data)
    
    # Get all reviews
    response = client.get("/api/v1/reviews/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1

def test_get_review_by_id_success(client, sample_review_data):
    """Test getting review by valid ID"""
    # Create review
    create_response = client.post("/api/v1/reviews/", json=sample_review_data)
    review_id = create_response.get_json()["id"]
    
    # Get review
    response = client.get(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == review_id
    assert data["rating"] == sample_review_data["rating"]

def test_get_review_invalid_id(client):
    """Test getting review with invalid ID"""
    response = client.get("/api/v1/reviews/invalid-id")
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_get_review_nonexistent_id(client):
    """Test getting review with non-existent ID"""
    response = client.get("/api/v1/reviews/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert "error" in response.get_json()

# ========== UPDATE REVIEW TESTS ==========

def test_update_review_success(client, sample_review_data):
    """Test successful review update"""
    # Create review
    create_response = client.post("/api/v1/reviews/", json=sample_review_data)
    review_id = create_response.get_json()["id"]
    
    # Update review
    update_data = {
        "rating": 4,
        "comment": "Updated comment"
    }
    response = client.put(f"/api/v1/reviews/{review_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["rating"] == 4
    assert data["comment"] == "Updated comment"

def test_update_review_partial(client, sample_review_data):
    """Test partial review update"""
    # Create review
    create_response = client.post("/api/v1/reviews/", json=sample_review_data)
    review_id = create_response.get_json()["id"]
    
    # Update only rating
    response = client.put(f"/api/v1/reviews/{review_id}", 
                         json={"rating": 3})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["rating"] == 3
    assert data["comment"] == sample_review_data["comment"]  # Unchanged

def test_update_review_invalid_rating(client, sample_review_data):
    """Test updating review with invalid rating"""
    # Create review
    create_response = client.post("/api/v1/reviews/", json=sample_review_data)
    review_id = create_response.get_json()["id"]
    
    # Update with invalid rating
    response = client.put(f"/api/v1/reviews/{review_id}", 
                         json={"rating": 10})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_update_review_empty_comment(client, sample_review_data):
    """Test updating review with empty comment"""
    # Create review
    create_response = client.post("/api/v1/reviews/", json=sample_review_data)
    review_id = create_response.get_json()["id"]
    
    # Update with empty comment
    response = client.put(f"/api/v1/reviews/{review_id}", 
                         json={"comment": ""})
    assert response.status_code == 400
    assert "error" in response.get_json()

# ========== DELETE REVIEW TESTS ==========

def test_delete_review_success(client, sample_review_data):
    """Test successful review deletion"""
    # Create review
    create_response = client.post("/api/v1/reviews/", json=sample_review_data)
    review_id = create_response.get_json()["id"]
    
    # Delete review
    response = client.delete(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 200
    assert "message" in response.get_json()
    
    # Verify review is gone
    get_response = client.get(f"/api/v1/reviews/{review_id}")
    assert get_response.status_code == 404

def test_delete_review_not_found(client):
    """Test deleting non-existent review"""
    response = client.delete("/api/v1/reviews/123")
    assert response.status_code == 404
    assert "error" in response.get_json()

# ========== PLACE REVIEWS TESTS ==========

def test_get_place_reviews_success(client, test_place, sample_review_data):
    """Test getting all reviews for a place"""
    # Create a review
    client.post("/api/v1/reviews/", json=sample_review_data)
    
    # Get place reviews
    response = client.get(f"/api/v1/places/{test_place['id']}/reviews")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert data[0]["place_id"] == test_place["id"]

def test_get_place_reviews_invalid_place(client):
    """Test getting reviews for invalid place"""
    response = client.get("/api/v1/places/invalid-id/reviews")
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_get_place_reviews_empty(client, test_place):
    """Test getting reviews for place with no reviews"""
    response = client.get(f"/api/v1/places/{test_place['id']}/reviews")
    assert response.status_code == 200
    assert response.get_json() == []

# ========== REVIEW MODEL TESTS ==========

def test_review_model_creation():
    """Test Review model initialization"""
    review = Review(
        rating=5,
        comment="Great place!",
        user_id="user-123",
        place_id="place-456"
    )
    
    assert review.rating == 5
    assert review.comment == "Great place!"
    assert review.user_id == "user-123"
    assert review.place_id == "place-456"
    assert review.id is not None
    assert review.created_at is not None
    assert review.updated_at is not None

def test_review_validate():
    """Test review validation method"""
    # Valid review
    review1 = Review(5, "Good", "user-1", "place-1")
    assert review1.validate() == True
    
    # Invalid rating
    review2 = Review(6, "Good", "user-1", "place-1")
    assert review2.validate() == False
    
    # Empty comment
    review3 = Review(5, "", "user-1", "place-1")
    assert review3.validate() == False

def test_review_save_method():
    """Test save method updates timestamp"""
    review = Review(5, "Test", "user-1", "place-1")
    original_updated = review.updated_at
    review.save()
    assert review.updated_at > original_updated

def test_review_to_dict():
    """Test to_dict method"""
    review = Review(5, "Test comment", "user-123", "place-456")
    review_dict = review.to_dict()
    
    assert "id" in review_dict
    assert "rating" in review_dict
    assert "comment" in review_dict
    assert "user_id" in review_dict
    assert "place_id" in review_dict
    assert "created_at" in review_dict
    assert "updated_at" in review_dict
    assert review_dict["rating"] == 5

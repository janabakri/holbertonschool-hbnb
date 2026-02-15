"""
Unit tests for User endpoints and models
"""
import pytest
from app import create_app
from app.models.user import User

@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@test.com",
        "password": "password123",
        "first_name": "Rama",
        "last_name": "Alshehri"
    }

@pytest.fixture
def created_user(client, sample_user_data):
    """Create a user and return its ID"""
    response = client.post("/api/v1/users/", json=sample_user_data)
    return response.get_json()["id"]

# ========== CREATE USER TESTS ==========

def test_create_user_success(client, sample_user_data):
    """Test successful user creation"""
    response = client.post("/api/v1/users/", json=sample_user_data)
    
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["email"] == sample_user_data["email"]
    assert data["first_name"] == sample_user_data["first_name"]
    assert data["last_name"] == sample_user_data["last_name"]
    assert "password" not in data  # Password should not be returned

def test_create_user_missing_email(client):
    """Test user creation with missing email"""
    response = client.post("/api/v1/users/", json={
        "password": "1234",
        "first_name": "Rama",
        "last_name": "Alshehri"
    })
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_user_missing_password(client):
    """Test user creation with missing password"""
    response = client.post("/api/v1/users/", json={
        "email": "test@test.com",
        "first_name": "Rama",
        "last_name": "Alshehri"
    })
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_user_empty_fields(client):
    """Test user creation with empty fields"""
    response = client.post("/api/v1/users/", json={
        "email": "",
        "password": "",
        "first_name": "",
        "last_name": ""
    })
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_user_invalid_email_format(client):
    """Test user creation with invalid email format"""
    response = client.post("/api/v1/users/", json={
        "email": "invalid-email",
        "password": "1234",
        "first_name": "Rama",
        "last_name": "Alshehri"
    })
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_duplicate_email(client, sample_user_data):
    """Test creating user with existing email"""
    # Create first user
    client.post("/api/v1/users/", json=sample_user_data)
    
    # Try to create second user with same email
    response = client.post("/api/v1/users/", json=sample_user_data)
    assert response.status_code == 409
    assert "error" in response.get_json()

# ========== GET USERS TESTS ==========

def test_get_all_users_empty(client):
    """Test getting all users when none exist"""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_all_users_with_data(client, sample_user_data):
    """Test getting all users after creation"""
    # Create a user
    client.post("/api/v1/users/", json=sample_user_data)
    
    # Get all users
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["email"] == sample_user_data["email"]

def test_get_user_by_id_success(client, created_user):
    """Test getting user by valid ID"""
    response = client.get(f"/api/v1/users/{created_user}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == created_user

def test_get_user_by_invalid_id(client):
    """Test getting user with invalid ID"""
    response = client.get("/api/v1/users/invalid-id-123")
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_get_user_nonexistent_id(client):
    """Test getting user with non-existent ID"""
    response = client.get("/api/v1/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert "error" in response.get_json()

# ========== UPDATE USER TESTS ==========

def test_update_user_success(client, created_user):
    """Test successful user update"""
    update_data = {
        "first_name": "Updated",
        "last_name": "Name"
    }
    
    response = client.put(f"/api/v1/users/{created_user}", json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Name"
    assert data["id"] == created_user

def test_update_user_partial(client, created_user):
    """Test partial user update"""
    update_data = {
        "first_name": "OnlyFirst"
    }
    
    response = client.put(f"/api/v1/users/{created_user}", json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["first_name"] == "OnlyFirst"
    # Other fields should remain unchanged

def test_update_user_invalid_id(client):
    """Test updating user with invalid ID"""
    response = client.put("/api/v1/users/invalid-id", json={"first_name": "New"})
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_update_user_empty_data(client, created_user):
    """Test updating with empty data"""
    response = client.put(f"/api/v1/users/{created_user}", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_update_user_invalid_email(client, created_user):
    """Test updating with invalid email"""
    response = client.put(f"/api/v1/users/{created_user}", 
                         json={"email": "invalid-email"})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_update_user_empty_name(client, created_user):
    """Test updating with empty name"""
    response = client.put(f"/api/v1/users/{created_user}", 
                         json={"first_name": ""})
    assert response.status_code == 400
    assert "error" in response.get_json()

# ========== USER MODEL TESTS ==========

def test_user_model_creation():
    """Test User model initialization"""
    user = User(
        email="model@test.com",
        password="secret123",
        first_name="Model",
        last_name="Test"
    )
    
    assert user.email == "model@test.com"
    assert user.first_name == "Model"
    assert user.last_name == "Test"
    assert user.id is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.places == []
    assert user.reviews == []
    assert user.is_admin == False

def test_user_get_full_name():
    """Test get_full_name method"""
    user = User(
        email="test@test.com",
        password="1234",
        first_name="Rama",
        last_name="Alshehri"
    )
    assert user.get_full_name() == "Rama Alshehri"

def test_user_password_hashing():
    """Test password hashing"""
    user = User(
        email="test@test.com",
        password="secret123",
        first_name="Test",
        last_name="User"
    )
    
    # Password should be hashed, not stored as plain text
    assert user.password_hash != "secret123"
    assert len(user.password_hash) == 64  # SHA256 produces 64 chars
    
    # Verify password works
    assert user.verify_password("secret123") == True
    assert user.verify_password("wrong") == False

def test_user_to_dict_no_password():
    """Test to_dict method doesn't include password"""
    user = User(
        email="test@test.com",
        password="secret123",
        first_name="Test",
        last_name="User"
    )
    
    user_dict = user.to_dict()
    assert "password_hash" not in user_dict
    assert "email" in user_dict
    assert "first_name" in user_dict
    assert "last_name" in user_dict
    assert "id" in user_dict
    assert "created_at" in user_dict
    assert "updated_at" in user_dict

def test_user_save_updates_timestamp():
    """Test save method updates updated_at"""
    user = User(
        email="test@test.com",
        password="1234",
        first_name="Test",
        last_name="User"
    )
    
    original_updated = user.updated_at
    user.save()
    assert user.updated_at > original_updated

import unittest
import json
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
    
    def test_1_create_user_success(self):
        """Test successful user creation"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], "John")
        self.assertEqual(data['last_name'], "Doe")
        self.assertEqual(data['email'], "john.doe@example.com")
    
    def test_2_create_user_empty_first_name(self):
        """Test user creation with empty first name"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_3_create_user_invalid_email(self):
        """Test user creation with invalid email format"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "Invalid email format")
    
    def test_4_create_user_duplicate_email(self):
        """Test user creation with duplicate email"""
        # Create first user
        self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "duplicate@example.com"
        })
        
        # Try to create second user with same email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "duplicate@example.com"
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "Email already exists")
    
    def test_5_get_all_users(self):
        """Test getting all users"""
        # Create test users
        self.client.post('/api/v1/users/', json={
            "first_name": "User1",
            "last_name": "Test",
            "email": "user1@test.com"
        })
        self.client.post('/api/v1/users/', json={
            "first_name": "User2",
            "last_name": "Test",
            "email": "user2@test.com"
        })
        
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_6_get_user_by_id(self):
        """Test getting a user by ID"""
        # Create a user
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.get@example.com"
        })
        user_data = json.loads(create_response.data)
        user_id = user_data['id']
        
        # Get user by ID
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], "John")
        self.assertEqual(data['email'], "john.get@example.com")
    
    def test_7_get_user_not_found(self):
        """Test getting a non-existent user"""
        response = self.client.get('/api/v1/users/non-existent-id')
        self.assertEqual(response.status_code, 404)
    
    def test_8_update_user(self):
        """Test updating a user"""
        # Create a user
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.update@example.com"
        })
        user_data = json.loads(create_response.data)
        user_id = user_data['id']
        
        # Update user
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Johnathan",
            "last_name": "Doe",
            "email": "johnathan.update@example.com"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], "Johnathan")
        self.assertEqual(data['email'], "johnathan.update@example.com")

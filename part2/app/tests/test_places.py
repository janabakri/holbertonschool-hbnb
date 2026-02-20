import unittest
import json
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
        
        # Create a test user to be owner
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "owner@example.com"
        })
        self.owner_id = json.loads(user_response.data)['id']
    
    def test_1_create_place_success(self):
        """Test successful place creation"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beautiful Beach House",
            "description": "A lovely house by the beach",
            "price": 150.50,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Beautiful Beach House")
        self.assertEqual(float(data['price']), 150.50)
    
    def test_2_create_place_empty_title(self):
        """Test place creation with empty title"""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": 150.50,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
    
    def test_3_create_place_negative_price(self):
        """Test place creation with negative price"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": -50.00,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
    
    def test_4_create_place_invalid_latitude(self):
        """Test place creation with invalid latitude"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": 150.50,
            "latitude": 100.0,
            "longitude": -74.0060,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
    
    def test_5_create_place_invalid_longitude(self):
        """Test place creation with invalid longitude"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": 150.50,
            "latitude": 40.7128,
            "longitude": 200.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)
    
    def test_6_get_all_places(self):
        """Test getting all places"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_7_get_place_by_id(self):
        """Test getting a place by ID"""
        # Create a place
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 100.00,
            "owner_id": self.owner_id
        })
        place_data = json.loads(create_response.data)
        place_id = place_data['id']
        
        # Get place by ID
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Test Place")
        self.assertIn('owner', data)
    
    def test_8_get_place_not_found(self):
        """Test getting a non-existent place"""
        response = self.client.get('/api/v1/places/non-existent-id')
        self.assertEqual(response.status_code, 404)

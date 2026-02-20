import unittest
import json
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
    
    def test_1_create_amenity_success(self):
        """Test successful amenity creation"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], "WiFi")
    
    def test_2_create_amenity_empty_name(self):
        """Test amenity creation with empty name"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_3_create_amenity_missing_name(self):
        """Test amenity creation with missing name"""
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)
    
    def test_4_get_all_amenities(self):
        """Test getting all amenities"""
        # Create test amenities
        self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        self.client.post('/api/v1/amenities/', json={"name": "Pool"})
        
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)
    
    def test_5_get_amenity_by_id(self):
        """Test getting an amenity by ID"""
        # Create an amenity
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "Parking"
        })
        amenity_data = json.loads(create_response.data)
        amenity_id = amenity_data['id']
        
        # Get amenity by ID
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Parking")
    
    def test_6_get_amenity_not_found(self):
        """Test getting a non-existent amenity"""
        response = self.client.get('/api/v1/amenities/non-existent-id')
        self.assertEqual(response.status_code, 404)
    
    def test_7_update_amenity(self):
        """Test updating an amenity"""
        # Create an amenity
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "Old Name"
        })
        amenity_data = json.loads(create_response.data)
        amenity_id = amenity_data['id']
        
        # Update amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "New Name"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "New Name")

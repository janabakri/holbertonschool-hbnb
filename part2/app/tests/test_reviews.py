import unittest
import json
from app import create_app

class TestReviewEndpoints(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
        
        # Create a test user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "reviewer@example.com"
        })
        self.user_id = json.loads(user_response.data)['id']
        
        # Create a test place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 100.00,
            "owner_id": self.user_id
        })
        self.place_id = json.loads(place_response.data)['id']
    
    def test_1_create_review_success(self):
        """Test successful review creation"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place! Very clean and comfortable.",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['text'], "Great place! Very clean and comfortable.")
        self.assertEqual(data['rating'], 5)
    
    def test_2_create_review_empty_text(self):
        """Test review creation with empty text"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
    
    def test_3_create_review_invalid_rating(self):
        """Test review creation with invalid rating"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Good place",
            "rating": 10,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
    
    def test_4_get_reviews_by_place(self):
        """Test getting all reviews for a place"""
        # Create a review
        self.client.post('/api/v1/reviews/', json={
            "text": "First review",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        
        # Get reviews by place
        response = self.client.get(f'/api/v1/reviews/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_5_update_review(self):
        """Test updating a review"""
        # Create a review
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Original review",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_data = json.loads(create_response.data)
        review_id = review_data['id']
        
        # Update review
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review",
            "rating": 4
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['text'], "Updated review")
        self.assertEqual(data['rating'], 4)
    
    def test_6_delete_review(self):
        """Test deleting a review"""
        # Create a review
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Review to delete",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_data = json.loads(create_response.data)
        review_id = review_data['id']
        
        # Delete review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify review is deleted
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)

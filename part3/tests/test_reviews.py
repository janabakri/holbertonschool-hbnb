import unittest
import json
from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from flask_jwt_extended import create_access_token

class TestReviews(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        
        self.owner = User(
            first_name='Owner',
            last_name='User',
            email='owner@test.com',
            password='password123'
        )
        db.session.add(self.owner)
        
        
        self.user = User(
            first_name='Reviewer',
            last_name='User',
            email='reviewer@test.com',
            password='password123'
        )
        db.session.add(self.user)
        db.session.commit()
        
        
        self.place = Place(
            title='Test Place',
            description='Test Description',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.owner.id
        )
        db.session.add(self.place)
        db.session.commit()
        
        self.user_token = create_access_token(identity=str(self.user.id))
        self.owner_token = create_access_token(identity=str(self.owner.id))
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_review(self):
        
        response = self.client.post('/api/v1/reviews/',
            json={
                'text': 'Great place!',
                'rating': 5,
                'user_id': self.user.id,
                'place_id': self.place.id
            },
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['text'], 'Great place!')
        self.assertEqual(data['rating'], 5)
    
    def test_cannot_review_own_place(self):
        
        response = self.client.post('/api/v1/reviews/',
            json={
                'text': 'My own place',
                'rating': 5,
                'user_id': self.owner.id,
                'place_id': self.place.id
            },
            headers={'Authorization': f'Bearer {self.owner_token}'}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_duplicate_review_forbidden(self):
        
        
        self.client.post('/api/v1/reviews/',
            json={
                'text': 'First review',
                'rating': 4,
                'user_id': self.user.id,
                'place_id': self.place.id
            },
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        
        
        response = self.client.post('/api/v1/reviews/',
            json={
                'text': 'Second review',
                'rating': 3,
                'user_id': self.user.id,
                'place_id': self.place.id
            },
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()

"""
Test suite for Authentication endpoints.
Tests login, token generation, and protected endpoints.
"""
import unittest
import json
from hbnb.app import create_app
from hbnb.app.extensions import db
from hbnb.app.models.user import Account
from flask_jwt_extended import create_access_token


class TestAuthAPI(unittest.TestCase):
    """Test cases for Authentication API endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
        
        # Create test user
        self.user = Account(
            first_name='Test',
            last_name='User',
            email='auth@test.com',
            plain_password='TestPass123',
            is_admin=False
        )
        db.session.add(self.user)
        db.session.commit()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    # =====================================================
    # POST /api/v1/auth/login - User login
    # =====================================================
    
    def test_login_success(self):
        """Test successful login with valid credentials"""
        credentials = {
            'email': 'auth@test.com',
            'password': 'TestPass123'
        }
        
        response = self.client.post(
            '/api/v1/auth/login',
            json=credentials
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check response structure
        self.assertIn('access_token', data)
        self.assertIn('user', data)
        
        # Check user data
        user_data = data['user']
        self.assertEqual(user_data['email'], 'auth@test.com')
        self.assertEqual(user_data['first_name'], 'Test')
        self.assertEqual(user_data['last_name'], 'User')
        self.assertFalse(user_data['is_admin'])
        
        # Password should not be in response
        self.assertNotIn('password', user_data)
    
    def test_login_wrong_password(self):
        """Test login with incorrect password"""
        credentials = {
            'email': 'auth@test.com',
            'password': 'WrongPass123'
        }
        
        response = self.client.post(
            '/api/v1/auth/login',
            json=credentials
        )
        
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('Invalid credentials', str(data))
    
    def test_login_email_not_found(self):
        """Test login with non-existent email"""
        credentials = {
            'email': 'nonexistent@test.com',
            'password': 'TestPass123'
        }
        
        response = self.client.post(
            '/api/v1/auth/login',
            json=credentials
        )
        
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('Invalid credentials', str(data))
    
    def test_login_missing_fields(self):
        """Test login with missing fields"""
        # Missing password
        response = self.client.post(
            '/api/v1/auth/login',
            json={'email': 'auth@test.com'}
        )
        self.assertEqual(response.status_code, 400)
        
        # Missing email
        response = self.client.post(
            '/api/v1/auth/login',
            json={'password': 'TestPass123'}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_login_empty_body(self):
        """Test login with empty request body"""
        response = self.client.post('/api/v1/auth/login', json={})
        self.assertEqual(response.status_code, 400)
    
    # =====================================================
    # Admin login test
    # =====================================================
    
    def test_login_admin_user(self):
        """Test login with admin user"""
        # Create admin user
        admin = Account(
            first_name='Admin',
            last_name='User',
            email='admin@auth.com',
            plain_password='AdminPass123',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        
        credentials = {
            'email': 'admin@auth.com',
            'password': 'AdminPass123'
        }
        
        response = self.client.post(
            '/api/v1/auth/login',
            json=credentials
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check admin flag in user data
        self.assertTrue(data['user']['is_admin'])
        
        # Token should contain admin claim
        # (We'll test claims in a separate test)
    
    # =====================================================
    # Protected endpoint test
    # =====================================================
    
    def test_protected_endpoint_with_token(self):
        """Test accessing protected endpoint with valid token"""
        token = create_access_token(
            identity=self.user.user_id,
            additional_claims={'is_admin': self.user.is_administrator}
        )
        
        response = self.client.get(
            '/api/v1/protected/',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Access granted', str(data))
    
    def test_protected_endpoint_no_token(self):
        """Test accessing protected endpoint without token"""
        response = self.client.get('/api/v1/protected/')
        self.assertEqual(response.status_code, 401)
    
    def test_protected_endpoint_invalid_token(self):
        """Test accessing protected endpoint with invalid token"""
        response = self.client.get(
            '/api/v1/protected/',
            headers={'Authorization': 'Bearer invalid.token.here'}
        )
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity
    
    def test_admin_protected_endpoint_regular_user(self):
        """Test admin-only endpoint with regular user token"""
        token = create_access_token(
            identity=self.user.user_id,
            additional_claims={'is_admin': False}
        )
        
        response = self.client.get(
            '/api/v1/protected/admin',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_admin_protected_endpoint_admin_user(self):
        """Test admin-only endpoint with admin token"""
        # Create admin
        admin = Account(
            first_name='Admin',
            last_name='User',
            email='admin2@test.com',
            plain_password='AdminPass123',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        
        token = create_access_token(
            identity=admin.user_id,
            additional_claims={'is_admin': True}
        )
        
        response = self.client.get(
            '/api/v1/protected/admin',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

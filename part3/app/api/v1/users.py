"""User account management endpoints for the HBnB platform"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from hbnb.app.services.facade import HBnBFacade

# Create namespace for user operations
user_namespace = Namespace('users', description='User account management')

# Initialize service facade
service_facade = HBnBFacade()

def verify_admin_privileges():
    """Check if authenticated user has administrator rights"""
    token_claims = get_jwt()
    return token_claims.get('is_admin', False)

# Request validation schema for user registration
registration_schema = user_namespace.model('UserRegistration', {
    'first_name': fields.String(
        required=True, 
        description='Given name',
        min_length=2, 
        max_length=50,
        example='John'
    ),
    'last_name': fields.String(
        required=True, 
        description='Family name',
        min_length=2, 
        max_length=50,
        example='Smith'
    ),
    'email': fields.String(
        required=True, 
        description='Email address',
        example='john.smith@example.com'
    ),
    'password': fields.String(
        required=True, 
        description='Account password',
        example='SecurePass123!'
    ),
    'is_admin': fields.Boolean(
        description='Administrator privileges',
        default=False,
        example=False
    )
})

# Request validation schema for authentication
authentication_schema = user_namespace.model('UserAuthentication', {
    'email': fields.String(
        required=True, 
        description='Email address',
        example='john.smith@example.com'
    ),
    'password': fields.String(
        required=True, 
        description='Account password',
        example='SecurePass123!'
    )
})

# Response schema for user data (excluding sensitive information)
user_profile_schema = user_namespace.model('UserProfile', {
    'identifier': fields.String(attribute='id', description='User system ID'),
    'given_name': fields.String(attribute='first_name', description='User given name'),
    'family_name': fields.String(attribute='last_name', description='User family name'),
    'email_address': fields.String(attribute='email', description='User email address'),
    'administrator': fields.Boolean(attribute='is_admin', description='Administrator status'),
    'account_created': fields.DateTime(attribute='created_at', description

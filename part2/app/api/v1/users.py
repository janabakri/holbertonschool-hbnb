from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Define models for Swagger
user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address'),
    'is_admin': fields.Boolean(description='Admin status', default=False)
})

user_output_model = api.model('User', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email address'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_input_model)
    @api.marshal_with(user_output_model, code=201)
    @api.response(400, 'Validation Error')
    @api.response(409, 'Email already exists')
    def post(self):
        """Create a new user"""
        data = request.json
        result, status_code = facade.create_user(data)
        
        if status_code != 201:
            api.abort(status_code, result['error'])
        
        return result, status_code
    
    @api.marshal_list_with(user_output_model)
    def get(self):
        """Get all users"""
        result, status_code = facade.get_all_users()
        return result, status_code

@api.route('/<string:user_id>')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.marshal_with(user_output_model)
    def get(self, user_id):
        """Get a user by ID"""
        result, status_code = facade.get_user(user_id)
        
        if status_code != 200:
            api.abort(status_code, result['error'])
        
        return result, status_code
    
    @api.expect(user_input_model)
    @api.marshal_with(user_output_model)
    @api.response(400, 'Validation Error')
    @api.response(409, 'Email already exists')
    def put(self, user_id):
        """Update a user"""
        data = request.json
        result, status_code = facade.update_user(user_id, data)
        
        if status_code != 200:
            api.abort(status_code, result['error'])
        
        return result, status_code

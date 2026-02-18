"""
User API endpoints with all CRUD operations
"""
from flask_restx import Namespace, Resource, fields
from flask import request

api = Namespace("users", description="User operations")
from app.services.facade import HBnBFacade

facade = HBnBFacade()
# Request models
user_model = api.model("User", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
    "first_name": fields.String(required=True, description="First name"),
    "last_name": fields.String(required=True, description="Last name")
})

user_update_model = api.model("UserUpdate", {
    "email": fields.String(description="User email"),
    "first_name": fields.String(description="First name"),
    "last_name": fields.String(description="Last name")
})

# Response model (without password)
user_response = api.model("UserResponse", {
    "id": fields.String(description="User ID"),
    "email": fields.String(description="User email"),
    "first_name": fields.String(description="First name"),
    "last_name": fields.String(description="Last name"),
    "created_at": fields.String(description="Creation timestamp"),
    "updated_at": fields.String(description="Last update timestamp")
})


@api.route("/")
class UserList(Resource):
    @api.doc("create_user")
    @api.expect(user_model)
    @api.marshal_with(user_response, code=201)
    @api.response(400, "Validation Error")
    @api.response(409, "Email already exists")
    def post(self):
        """Create a new user"""
        data = request.json
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing field: {field}"}, 400
            if not data[field] or data[field].strip() == "":
                return {"error": f"{field} cannot be empty"}, 400
        
        # Validate email format
        if "@" not in data["email"]:
            return {"error": "Invalid email format"}, 400
        
        # Check for duplicate email
        existing_users = facade.get_all_users()
        for user in existing_users:
            if user.email == data["email"]:
                return {"error": "Email already exists"}, 409
        
        # Create user
        user = facade.create_user(data)
        return user.to_dict(), 201
    
    @api.doc("list_users")
    @api.marshal_list_with(user_response)
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200


@api.route("/<string:user_id>")
@api.param("user_id", "User identifier")
class UserResource(Resource):
    @api.doc("get_user")
    @api.marshal_with(user_response)
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200
    
    @api.doc("update_user")
    @api.expect(user_update_model)
    @api.marshal_with(user_response)
    @api.response(404, "User not found")
    @api.response(400, "Validation Error")
    def put(self, user_id):
        """Update user information"""
        data = request.json
        
        if not data:
            return {"error": "No data provided"}, 400
        
        # Validate email if provided
        if "email" in data:
            if "@" not in data["email"]:
                return {"error": "Invalid email format"}, 400
        
        # Validate names if provided
        for field in ["first_name", "last_name"]:
            if field in data and data[field].strip() == "":
                return {"error": f"{field} cannot be empty"}, 400
        
        user = facade.update_user(user_id, data)
        if not user:
            return {"error": "User not found"}, 404
        
        return user.to_dict(), 200
@api.doc("delete_user")
    @api.response(204, "User deleted")
    def delete(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        facade.delete_user(user_id)
        return {"message": "User deleted"}, 204

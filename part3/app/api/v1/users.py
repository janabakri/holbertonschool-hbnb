from flask_restx import Namespace, Resource, fields
from flask import request
from app.models.user import User
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')
facade = HBnBFacade()

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    def post(self):
        data = request.get_json()
        facade.create_user(data)
        return user.to_dict(), 201

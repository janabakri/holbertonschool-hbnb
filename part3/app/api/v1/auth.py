from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token
from app.models.user import User

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

@api.route('/login')
class LoginResource(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=user.id,
            additional_claims={'is_admin': user.is_admin}
        )
        return {'access_token': access_token}, 200

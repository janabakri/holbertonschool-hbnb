from flask_restx import Namespace, Resource, fields
from flask import request
from app.models.user import User
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

# تعريف namespace
api = Namespace('users', description='User operations')

# إنشاء facade
facade = HBnBFacade()

# نموذج البيانات (Schema) للـ POST
user_model = api.model('User', {
    'first_name': fields.String(required=True, description="User's first name"),
    'last_name': fields.String(required=True, description="User's last name"),
    'email': fields.String(required=True, description="User's email"),
    'password': fields.String(required=True, description="User's password")
})

# ---- Routes ----
@api.route('/')
class UserList(Resource):

    @api.expect(user_model)
    def post(self):
        """إنشاء مستخدم جديد"""
        data = request.get_json()
        if not data:
            return {"error": "Invalid input"}, 400

        user_dict, status = facade.create_user(data)
        return user_dict, status

    def get(self):
        """جلب كل المستخدمين"""
        users = facade.get_all_users()
        # تحويل كل المستخدمين إلى dict
        return [user.to_dict() for user in users], 200

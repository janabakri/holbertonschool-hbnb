from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'place_id': fields.String(required=True),
    'text': fields.String(required=True),
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        review = facade.create_review(user_id=user_id, **data)
        return review.to_dict(), 201

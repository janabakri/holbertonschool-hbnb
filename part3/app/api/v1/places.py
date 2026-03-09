from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

place_model = api.model('Place', {
    'name': fields.String(required=True),
    'description': fields.String,
})

@api.route('/')
class PlaceList(Resource):

    def get(self):
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200

    @jwt_required()
    @api.expect(place_model)
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return {"error": "Invalid input"}, 400

        place = facade.create_place(user_id=user_id, **data)
        return place.to_dict(), 201

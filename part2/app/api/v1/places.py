from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# Define models for Swagger
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name')
})

user_summary_model = api.model('UserSummary', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email')
})

place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})

place_output_model = api.model('Place', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'owner_id': fields.String(description='Owner ID'),
    'owner': fields.Nested(user_summary_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_input_model)
    @api.marshal_with(place_output_model, code=201)
    @api.response(400, 'Validation Error')
    @api.response(404, 'Owner not found')
    def post(self):
        """Create a new place"""
        data = request.json
        result, status_code = facade.create_place(data)
        
        if status_code != 201:
            api.abort(status_code, result['error'])
        
        return result, status_code
    
    @api.marshal_list_with(place_output_model)
    def get(self):
        """Get all places"""
        result, status_code = facade.get_all_places()
        return result, status_code

@api.route('/<string:place_id>')
@api.response(404, 'Place not found')
class PlaceResource(Resource):
    @api.marshal_with(place_output_model)
    def get(self, place_id):
        """Get a place by ID"""
        result, status_code = facade.get_place(place_id)
        
        if status_code != 200:
            api.abort(status_code, result['error'])
        
        return result, status_code
    
    @api.expect(place_input_model)
    @api.marshal_with(place_output_model)
    @api.response(400, 'Validation Error')
    def put(self, place_id):
        """Update a place"""
        data = request.json
        result, status_code = facade.update_place(place_id, data)
        
        if status_code != 200:
            api.abort(status_code, result['error'])
        
        return result, status_code

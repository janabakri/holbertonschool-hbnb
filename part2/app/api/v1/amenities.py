from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

# Define models for Swagger
amenity_input_model = api.model('AmenityInput', {
    'name': fields.String(required=True, description='Amenity name')
})

amenity_output_model = api.model('Amenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_input_model)
    @api.marshal_with(amenity_output_model, code=201)
    @api.response(400, 'Validation Error')
    def post(self):
        """Create a new amenity"""
        data = request.json
        result, status_code = facade.create_amenity(data)
        
        if status_code != 201:
            api.abort(status_code, result['error'])
        
        return result, status_code
    
    @api.marshal_list_with(amenity_output_model)
    def get(self):
        """Get all amenities"""
        result, status_code = facade.get_all_amenities()
        return result, status_code

@api.route('/<string:amenity_id>')
@api.response(404, 'Amenity not found')
class AmenityResource(Resource):
    @api.marshal_with(amenity_output_model)
    def get(self, amenity_id):
        """Get an amenity by ID"""
        result, status_code = facade.get_amenity(amenity_id)
        
        if status_code != 200:
            api.abort(status_code, result['error'])
        
        return result, status_code
    
    @api.expect(amenity_input_model)
    @api.marshal_with(amenity_output_model)
    @api.response(400, 'Validation Error')
    def put(self, amenity_id):
        """Update an amenity"""
        data = request.json
        result, status_code = facade.update_amenity(amenity_id, data)
        
        if status_code != 200:
            api.abort(status_code, result['error'])
        
        return result, status_code

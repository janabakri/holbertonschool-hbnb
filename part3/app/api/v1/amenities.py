from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

# Model for input validation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'Success')
    def get(self):
        """Get all amenities (public)"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200
    
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Admin access required')
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin access required'}, 403
        
        amenity_data = request.json
        
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details (public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200
    
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Admin access required')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin access required'}, 403
        
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        amenity_data = request.json
        
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return updated_amenity.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
    
    @api.response(200, 'Amenity deleted')
    @api.response(403, 'Admin access required')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity (admin only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin access required'}, 403
        
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully'}, 200

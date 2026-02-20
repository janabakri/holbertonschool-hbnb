from flask_restx import Namespace, Resource, fields
from flask import request, current_app

api = Namespace('reviews', description='Review operations')

# Define models for Swagger
review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='ID of the reviewer'),
    'place_id': fields.String(required=True, description='ID of the reviewed place')
})

review_output_model = api.model('Review', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='Reviewer ID'),
    'place_id': fields.String(description='Place ID'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_input_model)
    @api.marshal_with(review_output_model, code=201)
    @api.response(400, 'Validation Error')
    @api.response(404, 'User or Place not found')
    def post(self):
        """Create a new review"""
        # Get the shared facade instance from app config
        facade = current_app.config['facade']
        data = request.json
        result, status_code = facade.create_review(data)
        
        if status_code != 201:
            api.abort(status_code, result['error'])
        
        return result, status_code
    
    @api.marshal_list_with(review_output_model)
    def get(self):
        """Get all reviews"""
        facade = current_app.config['facade']
        result, status_code = facade.get_all_reviews()
        return result, status_code

@api.route('/<string:review_id>')
@api.response(404, 'Review not found')
class ReviewResource(Resource):
    @api.marshal_with(review_output_model)
    def get(self, review_id):
        """Get a review by ID"""
        facade = current_app.config['facade']
        result, status_code = facade.get_review(review_id)
        
        if status_code != 200:
            api.abort(status_code, result['error'])
        
        return result, status_code
    
    @api.expect(review_input_model)
    @api.marshal_with(review_output_model)
    @api.response(400, 'Validation Error')
    def put(self, review_id):
        """Update a review"""
        facade = current_app.config['facade']
        data = request.json
        result, status_code = facade.update_review(review_id, data)
        
        if status_code != 200:
            api.abort(status_code, result['error'])
        
        return result, status_code
    
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        facade = current_app.config['facade']
        result, status_code = facade.delete_review(review_id)
        
        if status_code != 200:
            api.abort(status_code, result['error'])
        
        return result, status_code

@api.route('/places/<string:place_id>/reviews')
@api.response(404, 'Place not found')
class PlaceReviewList(Resource):
    @api.marshal_list_with(review_output_model)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        facade = current_app.config['facade']
        result, status_code = facade.get_reviews_by_place(place_id)
        
        if status_code != 200:
            api.abort(status_code, result['error'])
        
        return result, status_code

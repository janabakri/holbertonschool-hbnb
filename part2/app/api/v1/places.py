"""
Place API endpoints with all validations
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace("places", description="Place operations")
facade = HBnBFacade()

# Request models
place_model = api.model("Place", {
    "title": fields.String(required=True, description="Place title"),
    "price_per_night": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True, description="Latitude (-90 to 90)"),
    "longitude": fields.Float(required=True, description="Longitude (-180 to 180)"),
    "owner_id": fields.String(required=True, description="Owner ID")
})

place_update_model = api.model("PlaceUpdate", {
    "title": fields.String(description="Place title"),
    "price_per_night": fields.Float(description="Price per night"),
    "latitude": fields.Float(description="Latitude (-90 to 90)"),
    "longitude": fields.Float(description="Longitude (-180 to 180)")
})

# Response model
place_response = api.model("PlaceResponse", {
    "id": fields.String(description="Place ID"),
    "title": fields.String(description="Place title"),
    "price_per_night": fields.Float(description="Price per night"),
    "latitude": fields.Float(description="Latitude"),
    "longitude": fields.Float(description="Longitude"),
    "owner_id": fields.String(description="Owner ID"),
    "created_at": fields.String(description="Creation timestamp"),
    "updated_at": fields.String(description="Last update timestamp"),
    "average_rating": fields.Float(description="Average rating")
})


@api.route("/")
class PlaceList(Resource):
    @api.doc("create_place")
    @api.expect(place_model)
    @api.marshal_with(place_response, code=201)
    @api.response(400, "Validation Error")
    @api.response(404, "Owner not found")
    def post(self):
        """Create a new place"""
        data = request.json
        
        # Validate required fields
        required_fields = ["title", "price_per_night", "latitude", "longitude", "owner_id"]
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing field: {field}"}, 400
        
        # Validate title
        if not data["title"] or data["title"].strip() == "":
            return {"error": "Title cannot be empty"}, 400
        
        # Validate price
        try:
            price = float(data["price_per_night"])
            if price <= 0:
                return {"error": "Price must be positive"}, 400
        except ValueError:
            return {"error": "Invalid price format"}, 400
        
        # Validate coordinates
        try:
            lat = float(data["latitude"])
            lon = float(data["longitude"])
            if lat < -90 or lat > 90:
                return {"error": "Latitude must be between -90 and 90"}, 400
            if lon < -180 or lon > 180:
                return {"error": "Longitude must be between -180 and 180"}, 400
        except ValueError:
            return {"error": "Invalid coordinate format"}, 400
        
        # Check if owner exists
        owner = facade.get_user(data["owner_id"])
        if not owner:
            return {"error": "Owner not found"}, 404
        
        place = facade.create_place(data)
        if not place:
            return {"error": "Failed to create place"}, 400
        
        return place.to_dict(), 201
    
    @api.doc("list_places")
    @api.marshal_list_with(place_response)
    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200


@api.route("/<string:place_id>")
@api.param("place_id", "Place identifier")
class PlaceResource(Resource):
    @api.doc("get_place")
    @api.marshal_with(place_response)
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200
    
    @api.doc("update_place")
    @api.expect(place_update_model)
    @api.marshal_with(place_response)
    @api.response(404, "Place not found")
    @api.response(400, "Validation Error")
    def put(self, place_id):
        """Update place information"""
        data = request.json
        
        if not data:
            return {"error": "No data provided"}, 400
        
        # Validate price if provided
        if "price_per_night" in data:
            try:
                price = float(data["price_per_night"])
                if price <= 0:
                    return {"error": "Price must be positive"}, 400
            except ValueError:
                return {"error": "Invalid price format"}, 400
        
        # Validate coordinates if provided
        if "latitude" in data:
            try:
                lat = float(data["latitude"])
                if lat < -90 or lat > 90:
                    return {"error": "Latitude must be between -90 and 90"}, 400
            except ValueError:
                return {"error": "Invalid latitude format"}, 400
        
        if "longitude" in data:
            try:
                lon = float(data["longitude"])
                if lon < -180 or lon > 180:
                    return {"error": "Longitude must be between -180 and 180"}, 400
            except ValueError:
                return {"error": "Invalid longitude format"}, 400
        
        place = facade.update_place(place_id, data)
        if not place:
            return {"error": "Place not found"}, 404
        
        return place.to_dict(), 200


@api.route("/<string:place_id>/amenities/<string:amenity_id>")
@api.param("place_id", "Place identifier")
@api.param("amenity_id", "Amenity identifier")
class PlaceAmenityResource(Resource):
    @api.doc("add_amenity_to_place")
    @api.response(200, "Amenity added")
    @api.response(404, "Place or amenity not found")
    def post(self, place_id, amenity_id):
        """Add amenity to place"""
        if facade.add_amenity_to_place(place_id, amenity_id):
            return {"message": "Amenity added successfully"}, 200
        return {"error": "Place or amenity not found"}, 404


@api.route("/<string:place_id>/reviews")
@api.param("place_id", "Place identifier")
class PlaceReviewsResource(Resource):
    @api.doc("get_place_reviews")
    @api.response(200, "Success")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        
        return [review.to_dict() for review in place.reviews], 200

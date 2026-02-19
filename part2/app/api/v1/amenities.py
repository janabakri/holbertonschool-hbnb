"""
Amenity API endpoints with all CRUD operations
"""
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import request

api = Namespace("amenities", description="Amenity operations")
facade = HBnBFacade()

amenity_model = api.model("Amenity", {
    "name": fields.String(required=True, description="Amenity name"),
    "description": fields.String(description="Amenity description")
})

amenity_update_model = api.model("AmenityUpdate", {
    "name": fields.String(description="Amenity name"),
    "description": fields.String(description="Amenity description")
})

amenity_response = api.model("AmenityResponse", {
    "id": fields.String(description="Amenity ID"),
    "name": fields.String(description="Amenity name"),
    "description": fields.String(description="Amenity description"),
    "created_at": fields.String(description="Creation timestamp"),
    "updated_at": fields.String(description="Last update timestamp")
})

@api.route("/")
class AmenityList(Resource):
    @api.doc("create_amenity")
    @api.expect(amenity_model)
    @api.marshal_with(amenity_response, code=201)
    @api.response(400, "Validation Error")
    def post(self):
        data = request.json

        if "name" not in data:
            return {"error": "Name is required"}, 400

        if not data["name"] or data["name"].strip() == "":
            return {"error": "Name cannot be empty"}, 400

        amenity = facade.create_amenity(data)
        return amenity.to_dict(), 201

    @api.doc("list_amenities")
    @api.marshal_list_with(amenity_response)
    def get(self):
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

@api.route("/<string:amenity_id>")
@api.param("amenity_id", "Amenity identifier")
class AmenityResource(Resource):
    @api.doc("get_amenity")
    @api.marshal_with(amenity_response)
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @api.doc("update_amenity")
    @api.expect(amenity_update_model)
    @api.marshal_with(amenity_response)
    @api.response(404, "Amenity not found")
    @api.response(400, "Validation Error")
    def put(self, amenity_id):
        data = request.json

        if not data:
            return {"error": "No data provided"}, 400

        if "name" in data and data["name"].strip() == "":
            return {"error": "Name cannot be empty"}, 400

        amenity = facade.update_amenity(amenity_id, data)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        return amenity.to_dict(), 200

    @api.doc("delete_amenity")
    @api.response(204, "Amenity deleted")
    @api.response(404, "Amenity not found")
    def delete(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        facade.delete_amenity(amenity_id)
        return "", 204

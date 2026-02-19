#!/usr/bin/python3
"""
Review API endpoints with all CRUD operations
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace("reviews", description="Review operations")
facade = HBnBFacade()

review_model = api.model("Review", {
    "rating": fields.Integer(required=True, min=1, max=5, description="Rating (1-5)"),
    "comment": fields.String(required=True, description="Review comment"),
    "user_id": fields.String(required=True, description="User ID"),
    "place_id": fields.String(required=True, description="Place ID")
})

review_update_model = api.model("ReviewUpdate", {
    "rating": fields.Integer(min=1, max=5, description="Rating (1-5)"),
    "comment": fields.String(description="Review comment")
})

review_response = api.model("ReviewResponse", {
    "id": fields.String(description="Review ID"),
    "rating": fields.Integer(description="Rating"),
    "comment": fields.String(description="Review comment"),
    "user_id": fields.String(description="User ID"),
    "place_id": fields.String(description="Place ID"),
    "created_at": fields.String(description="Creation timestamp"),
    "updated_at": fields.String(description="Last update timestamp")
})

@api.route("/")
class ReviewList(Resource):
    @api.doc("create_review")
    @api.expect(review_model)
    @api.marshal_with(review_response, code=201)
    @api.response(400, "Validation Error")
    @api.response(404, "User or place not found")
    def post(self):
        data = request.json

        required_fields = ["rating", "comment", "user_id", "place_id"]
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing field: {field}"}, 400

        if not data["comment"] or data["comment"].strip() == "":
            return {"error": "Comment cannot be empty"}, 400

        try:
            rating = int(data["rating"])
            if rating < 1 or rating > 5:
                return {"error": "Rating must be between 1 and 5"}, 400
        except ValueError:
            return {"error": "Rating must be an integer"}, 400

        user = facade.get_user(data["user_id"])
        place = facade.get_place(data["place_id"])
        if not user or not place:
            return {"error": "User or place not found"}, 404

        review = facade.create_review(data)
        if not review:
            return {"error": "Failed to create review"}, 400

        return review.to_dict(), 201

    @api.doc("list_reviews")
    @api.marshal_list_with(review_response)
    def get(self):
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route("/<string:review_id>")
@api.param("review_id", "Review identifier")
class ReviewResource(Resource):
    @api.doc("get_review")
    @api.marshal_with(review_response)
    @api.response(404, "Review not found")
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.doc("update_review")
    @api.expect(review_update_model)
    @api.marshal_with(review_response)
    @api.response(404, "Review not found")
    @api.response(400, "Validation Error")
    def put(self, review_id):
        data = request.json

        if not data:
            return {"error": "No data provided"}, 400

        if "comment" in data and data["comment"].strip() == "":
            return {"error": "Comment cannot be empty"}, 400

        if "rating" in data:
            try:
                rating = int(data["rating"])
                if rating < 1 or rating > 5:
                    return {"error": "Rating must be between 1 and 5"}, 400
            except ValueError:
                return {"error": "Rating must be an integer"}, 400

        review = facade.update_review(review_id, data)
        if not review:
            return {"error": "Review not found"}, 404

        return review.to_dict(), 200

    @api.doc("delete_review")
    @api.response(204, "Review deleted")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        facade.delete_review(review_id)
        return "", 204


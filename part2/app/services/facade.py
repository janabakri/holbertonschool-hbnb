#!/usr/bin/python3
"""Facade for HBnB project"""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

class HBnBFacade:
    """Facade to handle Users, Places, Amenities, and Reviews"""

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ------------------ HELPERS ------------------
    @staticmethod
    def _normalize_amenities_ids(payload: dict) -> list:
        ids = []

        if "amenities" in payload and isinstance(payload["amenities"], list):
            for item in payload["amenities"]:
                if isinstance(item, dict) and "id" in item:
                    ids.append(item["id"])
                elif isinstance(item, str):
                    ids.append(item)

        if "amenity_ids" in payload and isinstance(payload["amenity_ids"], list):
            ids.extend(payload["amenity_ids"])

        seen = set()
        cleaned = []
        for x in ids:
            if x and x not in seen:
                seen.add(x)
                cleaned.append(x)
        return cleaned

    def _resolve_amenities(self, amenities_ids: list) -> list:
        amenities = []
        for amenity_id in amenities_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)
        return amenities

    # ------------------ USERS ------------------
    def create_user(self, user_data):
        required = ("email", "first_name", "last_name")
        for field in required:
            if field not in user_data or user_data[field] in (None, ""):
                raise ValueError(f"{field} is required")

        if self.get_user_by_email(user_data["email"]):
            raise ValueError("Email already registered")

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if "email" in user_data and user_data["email"]:
            if user_data["email"] != user.email:
                existing = self.get_user_by_email(user_data["email"])
                if existing and existing.id != user_id:
                    raise ValueError("Email already registered")

        for field in ("first_name", "last_name", "email"):
            if field in user_data and user_data[field] is not None:
                setattr(user, field, user_data[field])

        user.save()
        self.user_repo.update(user_id, user)
        return user

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            return False
        self.user_repo.delete(user_id)
        return True

    # ------------------ AMENITIES ------------------
    def create_amenity(self, amenity_data):
        if "name" not in amenity_data or not amenity_data.get("name"):
            return {"error": "name is required"}, 400

        amenity = Amenity(
            name=amenity_data.get("name"),
            description=amenity_data.get("description", "")
        )
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        if "name" in amenity_data:
            if not amenity_data["name"]:
                return {"error": "name is required"}, 400
            amenity.name = amenity_data["name"]

        if "description" in amenity_data and amenity_data["description"] is not None:
            amenity.description = amenity_data["description"]

        amenity.save()
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False
        self.amenity_repo.delete(amenity_id)
        return True

    # ------------------ PLACES ------------------
    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = self._normalize_amenities_ids(place_data)
        amenities = self._resolve_amenities(amenity_ids)

        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description", ""),
            owner=owner,
            latitude=place_data.get("latitude", 0.0),
            longitude=place_data.get("longitude", 0.0),
            price=place_data.get("price", 0.0),
        )

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        for field in ("title", "description", "latitude", "longitude", "price"):
            if field in place_data:
                setattr(place, field, place_data[field])

        if "owner_id" in place_data:
            new_owner = self.get_user(place_data["owner_id"])
            if not new_owner:
                raise ValueError("New owner not found")
            place.owner = new_owner

        amenity_ids = self._normalize_amenities_ids(place_data)
        if amenity_ids:
            # Reset amenities
            place._amenities = []
            for amenity in self._resolve_amenities(amenity_ids):
                place.add_amenity(amenity)

        place.save()
        self.place_repo.update(place_id, place)
        return place

    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return False

        # Delete associated reviews
        for review in self.get_reviews_by_place(place_id):
            self.delete_review(review.id)

        self.place_repo.delete(place_id)
        return True

    # ------------------ REVIEWS ------------------
    def create_review(self, review_data):
        text = review_data.get("text")
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")
        rating = review_data.get("rating")

        if not text:
            raise ValueError("text is required")
        if not user_id:
            raise ValueError("user_id is required")
        if not place_id:
            raise ValueError("place_id is required")
        if rating is None:
            raise ValueError("rating is required")

        if not self.get_user(user_id):
            raise ValueError("User not found")
        if not self.get_place(place_id):
            raise ValueError("Place not found")

        if self.get_review_by_user_and_place(user_id, place_id):
            raise ValueError("Review already exists for this user and place")

        review = Review(
            text=text,
            rating=rating,
            user_id=user_id,
            place_id=place_id
        )
        self.review_repo.add(review)
        place = self.get_place(place_id)
        if place:
            place.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all() if getattr(r, "place_id", None) == place_id]

    def get_reviews_by_user(self, user_id):
        return [r for r in self.review_repo.get_all() if getattr(r, "user_id", None) == user_id]

    def get_review_by_user_and_place(self, user_id, place_id):
        for r in self.review_repo.get_all():
            if getattr(r, "user_id", None) == user_id and getattr(r, "place_id", None) == place_id:
                return r
        return None

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if "text" in review_data:
            if not review_data["text"]:
                raise ValueError("text is required")
            review.text = review_data["text"]

        if "rating" in review_data and review_data["rating"] is not None:
            review.rating = review_data["rating"]

        review.save()
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        place = self.get_place(review.place_id) if hasattr(review, "place_id") else None
        if place and hasattr(place, "remove_review"):
            place.remove_review(review)

        self.review_repo.delete(review_id)
        return True

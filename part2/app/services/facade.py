"""
Facade pattern for HBnB business logic (v2)
"""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    """Facade to handle all business operations"""

    def __init__(self):
        """Initialize repositories"""
        self.users = InMemoryRepository()
        self.places = InMemoryRepository()
        self.reviews = InMemoryRepository()
        self.amenities = InMemoryRepository()

    # ---------------- Users ----------------
    def create_user(self, data):
        user = User(**data)
        return self.users.add(user)

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_all_users(self):
        return self.users.get_all()

    def update_user(self, user_id, data):
        return self.users.update(user_id, data)

    def delete_user(self, user_id):
        return self.users.delete(user_id)

    # ---------------- Places ----------------
    def create_place(self, data):
        owner = self.users.get(data.get("owner_id"))
        if not owner:
            return None

        place_data = {
            "title": data.get("title"),
            "description": data.get("description", ""),
            "price_per_night": data.get("price_per_night", 0.0),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "owner_id": data.get("owner_id")
        }

        place = Place(**place_data)
        owner.places.append(place.id)
        self.users.update(owner.id, {"places": owner.places})
        return self.places.add(place)

    def get_place(self, place_id):
        return self.places.get(place_id)

    def get_all_places(self):
        return self.places.get_all()

    def update_place(self, place_id, data):
        return self.places.update(place_id, data)

    def delete_place(self, place_id):
        return self.places.delete(place_id)

    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.places.get(place_id)
        amenity = self.amenities.get(amenity_id)
        if not place or not amenity:
            return False

        if not hasattr(place, "amenities"):
            place.amenities = []
        if amenity_id not in place.amenities:
            place.amenities.append(amenity_id)

        if not hasattr(amenity, "place_ids"):
            amenity.place_ids = []
        if place_id not in amenity.place_ids:
            amenity.place_ids.append(place_id)

        self.places.update(place_id, {"amenities": place.amenities})
        self.amenities.update(amenity_id, {"place_ids": amenity.place_ids})
        return True

    # ---------------- Reviews ----------------
    def create_review(self, data):
        user = self.users.get(data.get("user_id"))
        place = self.places.get(data.get("place_id"))
        if not user or not place:
            return None

        review = Review(**data)

        if not hasattr(place, "reviews"):
            place.reviews = []
        place.reviews.append(review.id)
        self.places.update(place.id, {"reviews": place.reviews})

        if not hasattr(user, "reviews"):
            user.reviews = []
        user.reviews.append(review.id)
        self.users.update(user.id, {"reviews": user.reviews})

        return self.reviews.add(review)

    def get_review(self, review_id):
        return self.reviews.get(review_id)

    def get_all_reviews(self):
        return self.reviews.get_all()

    def update_review(self, review_id, data):
        return self.reviews.update(review_id, data)

    def delete_review(self, review_id):
        review = self.reviews.get(review_id)
        if not review:
            return None


        place = self.places.get(review.place_id)
        if place and hasattr(place, "reviews"):
            place.reviews = [r_id for r_id in place.reviews if r_id != review_id]
            self.places.update(place.id, {"reviews": place.reviews})

        user = self.users.get(review.user_id)
        if user and hasattr(user, "reviews"):
            user.reviews = [r_id for r_id in user.reviews if r_id != review_id]
            self.users.update(user.id, {"reviews": user.reviews})

        return self.reviews.delete(review_id)

    # ---------------- Amenities ----------------
    def create_amenity(self, data):
        amenity = Amenity(**data)
        return self.amenities.add(amenity)

    def get_amenity(self, amenity_id):
        return self.amenities.get(amenity_id)

    def get_all_amenities(self):
        return self.amenities.get_all()

    def update_amenity(self, amenity_id, data):
        return self.amenities.update(amenity_id, data)

    def delete_amenity(self, amenity_id):
        return self.amenities.delete(amenity_id)

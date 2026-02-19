from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.users = InMemoryRepository()
        self.places = InMemoryRepository()
        self.reviews = InMemoryRepository()
        self.amenities = InMemoryRepository()

    # ========== USER OPERATIONS ==========
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

    # ========== PLACE OPERATIONS ==========
    def create_place(self, data):
        """Create a new place"""
        from app.models.place import Place
        place = Place(
            name=data["name"],
            description=data.get("description", ""),
            price_per_night=float(data["price_per_night"]),
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            owner_id=data["owner_id"]
        )
        return self.places.add(place)

    def get_place(self, place_id):
        return self.places.get(place_id)

    def get_all_places(self):
        return self.places.get_all()

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if not place:
            return None
        for key, value in data.items():
            if hasattr(place, key):
                setattr(place, key, value)
        return place

    def delete_place(self, place_id):
        return self.places.delete(place_id)

    # ========== REVIEW OPERATIONS ==========
    def create_review(self, data):
        review = Review(**data)
        return self.reviews.add(review)

    def get_review(self, review_id):
        return self.reviews.get(review_id)

    def get_all_reviews(self):
        return self.reviews.get_all()

    def update_review(self, review_id, data):
        return self.reviews.update(review_id, data)

    def delete_review(self, review_id):
        return self.reviews.delete(review_id)

    # ========== AMENITY OPERATIONS ==========
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

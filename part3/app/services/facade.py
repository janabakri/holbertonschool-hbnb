from app.persistence.repository import (
    UserRepository,
    PlaceRepository,
    ReviewRepository,
    AmenityRepository
)
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.extensions import bcrypt

class HBnBFacade:
    def __init__(self):
        self.users = UserRepository()
        self.places = PlaceRepository()
        self.reviews = ReviewRepository()
        self.amenities = AmenityRepository()

    # ---------------- USERS ----------------
    def create_user(self, data: dict) -> tuple[dict, int]:
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
        user.set_password(data['password'])
        self.users.create(user)
        return user.to_dict(), 201

    def get_user_by_email(self, email: str):
        return self.users.get_by_email(email)

    # ---------------- PLACES ----------------
    def create_place(self, user_id: str, **data):
        place = Place(
            title=data['name'],
            price=data.get('price', 0.0),
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0),
            owner_id=user_id,
            description=data.get('description', "")
        )
        self.places.create(place)
        return place

    # ---------------- REVIEWS ----------------
    def create_review(self, user_id: str, **data):
        review = Review(
            text=data['text'],
            rating=data['rating'],
            user_id=user_id,
            place_id=data['place_id']
        )
        self.reviews.create(review)
        return review

    # ---------------- AMENITIES ----------------
    def create_amenity(self, **data):
        amenity = Amenity(
            name=data['name'],
            description=data.get('description', "")
        )
        self.amenities.create(amenity)
        return amenity

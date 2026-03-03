from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app import db


class UserRepository:
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def get_by_id(self, user_id):
        return User.query.get(user_id)

    def create(self, user):
        db.session.add(user)
        db.session.commit()
        return user


class PlaceRepository:
    def get_all(self):
        return Place.query.all()

    def get_by_id(self, place_id):
        return Place.query.get(place_id)

    def create(self, place):
        db.session.add(place)
        db.session.commit()
        return place


class ReviewRepository:
    def create(self, review):
        db.session.add(review)
        db.session.commit()
        return review


class AmenityRepository:
    def create(self, amenity):
        db.session.add(amenity)
        db.session.commit()
        return amenity

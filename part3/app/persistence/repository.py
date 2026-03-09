from app import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class UserRepository:
    def get_by_email(self, email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    def get_by_id(self, user_id: str) -> User | None:
        return User.query.get(user_id)

    def create(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user: User) -> User:
        db.session.commit()
        return user

    def delete(self, user: User) -> None:
        db.session.delete(user)
        db.session.commit()


class PlaceRepository:
    def get_all(self) -> list[Place]:
        return Place.query.all()

    def get_by_id(self, place_id: str) -> Place | None:
        return Place.query.get(place_id)

    def get_by_owner(self, owner_id: str) -> list[Place]:
        return Place.query.filter_by(owner_id=owner_id).all()

    def create(self, place: Place) -> Place:
        db.session.add(place)
        db.session.commit()
        return place

    def update(self, place: Place) -> Place:
        db.session.commit()
        return place

    def delete(self, place: Place) -> None:
        db.session.delete(place)
        db.session.commit()


class ReviewRepository:
    def get_by_id(self, review_id: str) -> Review | None:
        return Review.query.get(review_id)

    def get_by_place(self, place_id: str) -> list[Review]:
        return Review.query.filter_by(place_id=place_id).all()

    def get_by_user(self, user_id: str) -> list[Review]:
        return Review.query.filter_by(user_id=user_id).all()

    def create(self, review: Review) -> Review:
        db.session.add(review)
        db.session.commit()
        return review

    def update(self, review: Review) -> Review:
        db.session.commit()
        return review

    def delete(self, review: Review) -> None:
        db.session.delete(review)
        db.session.commit()


class AmenityRepository:
    def get_by_id(self, amenity_id: str) -> Amenity | None:
        return Amenity.query.get(amenity_id)

    def get_all(self) -> list[Amenity]:
        return Amenity.query.all()

    def create(self, amenity: Amenity) -> Amenity:
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def update(self, amenity: Amenity) -> Amenity:
        db.session.commit()
        return amenity

    def delete(self, amenity: Amenity) -> None:
        db.session.delete(amenity)
        db.session.commit()

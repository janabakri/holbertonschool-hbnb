# tests/test_crud.py
from app import create_app
from app.extensions import db, bcrypt
from app.services.facade import HBnBFacade
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

app = create_app("development")
facade = HBnBFacade()

with app.app_context():
    print("\n STARTING UNIFIED CRUD TESTS \n")

    # ------------------ USERS ------------------
    print("Users CRUD")

    # Create using Facade
    user_data = {"first_name": "Test", "last_name": "User", "email": "test@hbnb.com", "password": "123456"}
    user, status = facade.create_user(user_data)
    print("Created User (Facade):", user)

    # Read directly
    read_user = User.query.filter_by(email="test@hbnb.com").first()
    print("Read User (Direct):", read_user.first_name, read_user.last_name)

    # Update
    read_user.first_name = "UpdatedTest"
    db.session.commit()
    print("Updated User (Direct):", read_user.first_name)

    # Delete
    db.session.delete(read_user)
    db.session.commit()
    print("Deleted User (Direct):", read_user.email)

    # ------------------ PLACES ------------------
    print("\n Places CRUD")

    # Create using Facade
    user_for_place = facade.create_user({"first_name": "Owner", "last_name": "One", "email": "owner@hbnb.com", "password": "123456"})[0]
    place = facade.create_place(
        user_id=user_for_place["id"],
        name="Test Place",
        description="A nice test place",
        price=50.0,
        latitude=24.7,
        longitude=46.6
    )
    print("Created Place (Facade):", place.to_dict())

    # Read
    read_place = Place.query.get(place.id)
    print("Read Place (Direct):", read_place.title, read_place.price)

    # Update
    read_place.price = 75.0
    db.session.commit()
    print("Updated Place (Direct):", read_place.price)

    # Delete
    db.session.delete(read_place)
    db.session.commit()
    print("Deleted Place (Direct):", read_place.title)

    # ------------------ REVIEWS ------------------
    print("\n Reviews CRUD")

    # Create using Facade
    place_for_review = facade.create_place(
        user_id=user_for_place["id"],
        name="Review Place",
        price=60.0,
        latitude=24.7,
        longitude=46.6
    )
    review = facade.create_review(
        user_id=user_for_place["id"],
        text="Awesome place!",
        rating=5,
        place_id=place_for_review.id
    )
    print("Created Review (Facade):", review.to_dict())

    # Read
    read_review = Review.query.get(review.id)
    print("Read Review (Direct):", read_review.text, read_review.rating)

    # Update
    read_review.rating = 4
    db.session.commit()
    print("Updated Review (Direct):", read_review.rating)

    # Delete
    db.session.delete(read_review)
    db.session.commit()
    print("Deleted Review (Direct):", read_review.text)

    # ------------------ AMENITIES ------------------
    print("\n Amenities CRUD")

    # Create using Facade
    amenity = facade.create_amenity(name="Gym", description="Fitness room")
    print("Created Amenity (Facade):", amenity.to_dict())

    # Read
    read_amenity = Amenity.query.get(amenity.id)
    print("Read Amenity (Direct):", read_amenity.name)

    # Update
    read_amenity.description = "Updated Fitness room"
    db.session.commit()
    print("Updated Amenity (Direct):", read_amenity.description)

    # Delete
    db.session.delete(read_amenity)
    db.session.commit()
    print("Deleted Amenity (Direct):", read_amenity.name)

    print("\n ALL UNIFIED CRUD TESTS COMPLETED SUCCESSFULLY!")

class HBnBFacade:
    def __init__(self):
        self.places = PlaceRepository()
        self.reviews = ReviewRepository()
        self.amenities = AmenityRepository()

    # ---------------- PLACES ----------------
    def create_place(self, **data):
        place = Place(
            title=data["title"],
            price=data["price"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner_id=data["owner_id"],
            description=data.get("description", "")
        )
        self.places.create(place)
        return place.to_dict(), 201

    # ---------------- REVIEWS ----------------
    def create_review(self, **data):
        review = Review(
            text=data["text"],
            rating=data["rating"],
            user_id=data["user_id"],
            place_id=data["place_id"]
        )
        self.reviews.create(review)
        return review.to_dict(), 201

    # ---------------- AMENITIES ----------------
    def create_amenity(self, **data):
        amenity = Amenity(
            name=data["name"],
            description=data.get("description", "")
        )
        self.amenities.create(amenity)
        return amenity.to_dict(), 201

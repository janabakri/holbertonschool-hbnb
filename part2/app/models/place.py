import uuid
from datetime import datetime

class Place:
    def __init__(self, name, description, price_per_night, latitude, longitude, owner_id):
        """Initialize a new place with all required fields"""
        print("=" * 50)
        print("Place.__init__ called with:")
        print(f"  name: {name}")
        print(f"  description: {description}")
        print(f"  price_per_night: {price_per_night}")
        print(f"  latitude: {latitude}")
        print(f"  longitude: {longitude}")
        print(f"  owner_id: {owner_id}")
        print("=" * 50)
        
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.name = name
        self.description = description
        self.price_per_night = float(price_per_night)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id
        self.amenities = []
        self.reviews = []
        
        print("Place object created with ID:", self.id)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def add_review(self, review):
        self.reviews.append(review)

    def get_average_rating(self):
        if not self.reviews:
            return 0.0
        total = sum(review.rating for review in self.reviews)
        return round(total / len(self.reviews), 1)

    def to_dict(self):
        """Convert place object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price_per_night': self.price_per_night,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'average_rating': self.get_average_rating()
        }

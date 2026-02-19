import uuid
from datetime import datetime

class Place:
    def __init__(self, name, description, price_per_night, latitude, longitude, owner_id):
        """Initialize a new place"""
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

    def to_dict(self):
        """Convert object to dictionary"""
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

    def get_average_rating(self):
        if not self.reviews:
            return 0.0
        total = sum(review.rating for review in self.reviews)
        return round(total / len(self.reviews), 1)

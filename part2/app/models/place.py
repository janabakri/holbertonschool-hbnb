"""
Place model with relationships
"""
import uuid
from datetime import datetime

class Place:
    """Place model for HBnB application"""
    
    def __init__(self, name, description="", price_per_night=0.0, latitude=None, longitude=None, owner_id=None):
        """Initialize a new place"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.name = name
        self.description = description
        self.price_per_night = float(price_per_night)
        self.latitude = float(latitude) if latitude is not None else None
        self.longitude = float(longitude) if longitude is not None else None
        self.owner_id = owner_id
        self.amenities = []
        self.reviews = []
    
    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        self.amenities.append(amenity)
    
    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)
    
    def get_average_rating(self):
        """Calculate average rating from reviews"""
        if not self.reviews:
            return 0.0
        total = sum(review.rating for review in self.reviews)
        return round(total / len(self.reviews), 1)
    
    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert object to dictionary"""
        data = self.__dict__.copy()
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['average_rating'] = self.get_average_rating()
        
        # Convert amenities to dicts
        data['amenities'] = [a.to_dict() for a in self.amenities]
        
        # Convert reviews to dicts
        data['reviews'] = [r.to_dict() for r in self.reviews]
        
        return data

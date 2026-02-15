"""
Amenity model
"""
import uuid
from datetime import datetime

class Amenity:
    """Amenity model for HBnB application"""
    
    def __init__(self, name, description=""):
        """Initialize a new amenity"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.name = name
        self.description = description
        self.place_ids = []  # IDs of places with this amenity
    
    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert object to dictionary"""
        data = self.__dict__.copy()
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data

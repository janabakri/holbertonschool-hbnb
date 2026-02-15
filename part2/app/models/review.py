"""
Review model with validation
"""
import uuid
from datetime import datetime

class Review:
    """Review model for HBnB application"""
    
    def __init__(self, rating, comment, user_id, place_id):
        """Initialize a new review"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.rating = int(rating)
        self.comment = comment
        self.user_id = user_id
        self.place_id = place_id
    
    def validate(self):
        """Validate review data"""
        return 1 <= self.rating <= 5 and self.comment and self.comment.strip()
    
    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert object to dictionary"""
        data = self.__dict__.copy()
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data

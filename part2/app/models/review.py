from uuid import uuid4
from datetime import datetime

class Review:
    """Review model with validation"""
    
    def __init__(self, text, rating, user_id, place_id, **kwargs):
        self.id = kwargs.get('id', str(uuid4()))
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        if not value or not value.strip():
            raise ValueError("Review text cannot be empty")
        self._text = value.strip()
    
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value):
        try:
            rating = int(value)
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")
            self._rating = rating
        except (TypeError, ValueError):
            raise ValueError("Rating must be a valid integer")
    
    def update(self, data):
        """Update review attributes"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'user_id', 'place_id']:
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

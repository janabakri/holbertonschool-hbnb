import re
from uuid import uuid4
from datetime import datetime

class User:
    """User model with validation"""
    
    def __init__(self, first_name, last_name, email, **kwargs):
        self.id = kwargs.get('id', str(uuid4()))
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = kwargs.get('is_admin', False)
        self.places = []  # List of place IDs
        self.reviews = []  # List of review IDs
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if not value or not value.strip():
            raise ValueError("First name cannot be empty")
        self._first_name = value.strip()
    
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if not value or not value.strip():
            raise ValueError("Last name cannot be empty")
        self._last_name = value.strip()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not value or not value.strip():
            raise ValueError("Email cannot be empty")
        if not self.validate_email(value):
            raise ValueError("Invalid email format")
        self._email = value.strip()
    
    def update(self, data):
        """Update user attributes"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

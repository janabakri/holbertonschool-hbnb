#!/usr/bin/python3
"""
User model with password hashing
"""
import uuid
from datetime import datetime
import hashlib

class User:
    """User model for HBnB application"""
    
    def __init__(self, email, password, first_name, last_name):
        """Initialize a new user"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.email = email
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = False
        self.places = []  # IDs of places owned
        self.reviews = []  # IDs of reviews written
    
    def get_full_name(self):
        """Return full name of user"""
        return f"{self.first_name} {self.last_name}"
    
    def verify_password(self, password):
        """Verify password (for future use)"""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    
    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert object to dictionary without password"""
        data = self.__dict__.copy()
        data.pop("password_hash")  # Remove sensitive data
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data

from uuid import uuid4
from datetime import datetime

class Place:
    """Place model with validation"""
    
    def __init__(self, title, price, owner_id, **kwargs):
        self.id = kwargs.get('id', str(uuid4()))
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
        self.title = title
        self.description = kwargs.get('description', '')
        self.price = price
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.owner_id = owner_id
        self.reviews = []  # List of review IDs
        self.amenities = []  # List of amenity IDs
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        try:
            price = float(value)
            if price <= 0:
                raise ValueError("Price must be a positive number")
            self._price = price
        except (TypeError, ValueError):
            raise ValueError("Price must be a valid number")
    
    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        if value is None:
            self._latitude = None
            return
        try:
            lat = float(value)
            if lat < -90 or lat > 90:
                raise ValueError("Latitude must be between -90 and 90")
            self._latitude = lat
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a valid number")
    
    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        if value is None:
            self._longitude = None
            return
        try:
            lon = float(value)
            if lon < -180 or lon > 180:
                raise ValueError("Longitude must be between -180 and 180")
            self._longitude = lon
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a valid number")
    
    def update(self, data):
        """Update place attributes"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'owner_id']:
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def add_amenity(self, amenity_id):
        """Add amenity to place"""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
            self.updated_at = datetime.now()
    
    def remove_amenity(self, amenity_id):
        """Remove amenity from place"""
        if amenity_id in self.amenities:
            self.amenities.remove(amenity_id)
            self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert place to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

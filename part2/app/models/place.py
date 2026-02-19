#!/usr/bin/python3
"""Place module"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .review import Review
    from .amenity import Amenity


class Place:
    """Place entity representing rental properties."""

    def __init__(
        self,
        title: str,
        description: str,
        price: float,
        latitude: float,
        longitude: float,
        owner: User,
        **kwargs,
    ):
        # Handle ID, created_at, updated_at from kwargs or create new ones
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())
        
        # Set attributes (will use property setters)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        
        # Initialize collections
        self._reviews: List[Review] = []
        self._amenities: List[Amenity] = []

        if owner:
            owner.add_place(self)

    # ============= Properties with Validation =============

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Title is required")
        if len(value) > 100:
            raise ValueError("Title must be under 100 characters")
        self._title = value.strip()
        self.updated_at = datetime.utcnow()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if len(value) > 1000:
            raise ValueError("Description must be under 1000 characters")
        self._description = value.strip() if value else ""
        self.updated_at = datetime.utcnow()

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        try:
            value = float(value)
            if value <= 0:
                raise ValueError("Price must be greater than 0")
            if value > 1000000:
                raise ValueError("Price must be under 1,000,000")
        except (TypeError, ValueError):
            raise ValueError("Price must be a number")
        self._price = round(value, 2)
        self.updated_at = datetime.utcnow()

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        try:
            value = float(value)
            if not (-90 <= value <= 90):
                raise ValueError("Latitude must be between -90 and 90")
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a number")
        self._latitude = value
        self.updated_at = datetime.utcnow()

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        try:
            value = float(value)
            if not (-180 <= value <= 180):
                raise ValueError("Longitude must be between -180 and 180")
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a number")
        self._longitude = value
        self.updated_at = datetime.utcnow()

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, value: User):
        if value is None:
            raise ValueError("Owner ID is required")
        self._owner = value
        self.updated_at = datetime.utcnow()

    # ============= Relationship Properties =============

    @property
    def reviews(self) -> List[Review]:
        return self._reviews.copy()

    @property
    def amenities(self) -> List[Amenity]:
        return self._amenities.copy()

    # ============= Relationship Methods =============

    def add_review(self, review: Review):
        if review not in self._reviews:
            self._reviews.append(review)
            self.save()

    def add_amenity(self, amenity: Amenity):
        if amenity not in self._amenities:
            self._amenities.append(amenity)
            self.save()
            amenity.add_place(self)

    def remove_amenity(self, amenity: Amenity):
        """Remove amenity from place"""
        if amenity in self._amenities:
            self._amenities.remove(amenity)
            self.save()
            amenity.remove_place(self)

    # ============= Business Methods =============

    def save(self):
        """Save the place (update timestamp)"""
        self.updated_at = datetime.utcnow()
        # In a real app, this would persist to database/storage

    def create(self):
        """Create the place"""
        self.save()

    def update(self, data: dict):
        """Update place attributes from dictionary"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.save()

    def delete(self):
        """Delete the place"""
        # In a real app, this would remove from database/storage
        pass

    def list_reviews(self) -> List[Review]:
        """Get all reviews for this place"""
        return self.reviews

    def get_amenities(self) -> List[Amenity]:
        """Get all amenities for this place"""
        return self.amenities

    def get_average_rating(self) -> float:
        """Calculate average rating from all reviews"""
        if not self._reviews:
            return 0.0
        total = sum(r.rating for r in self._reviews)
        return round(total / len(self._reviews), 1)

    # ============= Validation =============

    def validate(self) -> bool:
        """Validate place data"""
        try:
            _ = self.title
            _ = self.price
            _ = self.latitude
            _ = self.longitude
            _ = self.owner
            return True
        except (ValueError, AttributeError):
            return False

    # ============= Serialization =============

    def to_dict(self) -> dict:
        """Convert place to dictionary representation"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id if self.owner else None,
            "amenity_ids": [a.id for a in self._amenities],
            "average_rating": self.get_average_rating(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __str__(self) -> str:
        return f"[Place] {self.title}"

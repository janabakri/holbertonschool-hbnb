"""
Facade pattern for business logic
"""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    """Facade to handle all business operations"""
    
    def __init__(self):
        """Initialize repositories"""
        self.users = InMemoryRepository()
        self.places = InMemoryRepository()
        self.reviews = InMemoryRepository()
        self.amenities = InMemoryRepository()
    
    # ========== USER OPERATIONS ==========
    def create_user(self, data):
        """Create a new user"""
        user = User(**data)
        return self.users.add(user)
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_all_users(self):
        """Get all users"""
        return self.users.get_all()
    
    def update_user(self, user_id, data):
        """Update user information"""
        return self.users.update(user_id, data)
    
    def delete_user(self, user_id):
        """Delete user"""
        return self.users.delete(user_id)
    
    # ========== PLACE OPERATIONS ==========
    def create_place(self, data):
        """Create a new place"""
        place = Place(**data)
        return self.places.add(place)
    
    def get_place(self, place_id):
        """Get place by ID"""
        return self.places.get(place_id)
    
    def get_all_places(self):
        """Get all places"""
        return self.places.get_all()
    
    def update_place(self, place_id, data):
        """Update place information"""
        return self.places.update(place_id, data)
    
    def delete_place(self, place_id):
        """Delete place"""
        return self.places.delete(place_id)
    
    # ========== REVIEW OPERATIONS ==========
    def create_review(self, data):
        """Create a new review"""
        review = Review(**data)
        return self.reviews.add(review)
    
    def get_review(self, review_id):
        """Get review by ID"""
        return self.reviews.get(review_id)
    
    def get_all_reviews(self):
        """Get all reviews"""
        return self.reviews.get_all()
    
    def update_review(self, review_id, data):
        """Update review"""
        return self.reviews.update(review_id, data)
    
    def delete_review(self, review_id):
        """Delete review"""
        return self.reviews.delete(review_id)
    
    # ========== AMENITY OPERATIONS ==========
    def create_amenity(self, data):
        """Create a new amenity"""
        amenity = Amenity(**data)
        return self.amenities.add(amenity)
    
    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenities.get(amenity_id)
    
    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenities.get_all()
    
    def update_amenity(self, amenity_id, data):
        """Update amenity"""
        return self.amenities.update(amenity_id, data)
    
    def delete_amenity(self, amenity_id):
        """Delete amenity"""
        return self.amenities.delete(amenity_id)

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
    
    # ========== PLACE OPERATIONS ==========
    
    def create_place(self, data):
        """Create a new place"""
        # Check if owner exists
        owner = self.users.get(data["owner_id"])
        if not owner:
            return None
        
        place = Place(**data)
        owner.places.append(place.id)
        self.users.update(owner.id, {"places": owner.places})
        
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
    
    def add_amenity_to_place(self, place_id, amenity_id):
        """Add amenity to place"""
        place = self.places.get(place_id)
        amenity = self.amenities.get(amenity_id)
        
        if not place or not amenity:
            return False
        
        place.add_amenity(amenity)
        amenity.place_ids.append(place_id)
        
        self.amenities.update(amenity_id, {"place_ids": amenity.place_ids})
        self.places.update(place_id, {"amenities": place.amenities})
        
        return True
    
    # ========== REVIEW OPERATIONS ==========
    
    def create_review(self, data):
        """Create a new review"""
        user = self.users.get(data["user_id"])
        place = self.places.get(data["place_id"])
        
        if not user or not place:
            return None
        
        review = Review(**data)
        if not review.validate():
            return None
        
        # Add to repositories
        self.reviews.add(review)
        
        # Add to place
        place.add_review(review)
        self.places.update(place.id, {"reviews": place.reviews})
        
        # Add to user
        user.reviews.append(review.id)
        self.users.update(user.id, {"reviews": user.reviews})
        
        return review
    
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
        """Delete a review"""
        review = self.reviews.get(review_id)
        if not review:
            return None
        
        # Remove from place
        place = self.places.get(review.place_id)
        if place:
            place.reviews = [r for r in place.reviews if r.id != review_id]
            self.places.update(place.id, {"reviews": place.reviews})
        
        # Remove from user
        user = self.users.get(review.user_id)
        if user:
            user.reviews = [r_id for r_id in user.reviews if r_id != review_id]
            self.users.update(user.id, {"reviews": user.reviews})
        
        return self.reviews.delete(review_id)

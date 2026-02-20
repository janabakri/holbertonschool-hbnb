from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
    
    # User methods
    def create_user(self, user_data):
        """Create a new user with validation"""
        try:
            # Check if email already exists
            existing_user = self.user_repo.get_by_attribute('email', user_data.get('email'))
            if existing_user:
                return {'error': 'Email already exists'}, 400
            
            user = User(**user_data)
            self.user_repo.add(user)
            return user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def get_user(self, user_id):
        """Get user by ID"""
        user = self.user_repo.get(user_id)
        if user:
            return user.to_dict(), 200
        return {'error': 'User not found'}, 404
    
    def get_all_users(self):
        """Get all users"""
        users = [user.to_dict() for user in self.user_repo.get_all()]
        return users, 200
    
    def update_user(self, user_id, user_data):
        """Update user"""
        user = self.user_repo.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        try:
            # Check if email is being changed and if it already exists
            if 'email' in user_data and user_data['email'] != user.email:
                existing_user = self.user_repo.get_by_attribute('email', user_data['email'])
                if existing_user:
                    return {'error': 'Email already exists'}, 400
            
            user.update(user_data)
            return user.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
    
    # Place methods
    def create_place(self, place_data):
        """Create a new place with validation"""
        try:
            owner_id = place_data.get('owner_id')
            print(f"\n=== DEBUG PLACE CREATION ===")
            print(f"Looking for owner with ID: {owner_id}")
            print(f"ID type: {type(owner_id)}")
            
            # Debug: List all users in repository
            all_users = self.user_repo.get_all()
            print(f"Total users in repo: {len(all_users)}")
            for u in all_users:
                print(f"  - ID: {u.id}")
                print(f"    Name: {u.first_name} {u.last_name}")
                print(f"    Email: {u.email}")
                print(f"    Has places attr: {hasattr(u, 'places')}")
            
            # Verify owner exists
            owner = self.user_repo.get(owner_id)
            print(f"Owner found: {owner is not None}")
            
            if not owner:
                print(f"Owner NOT found with ID: {owner_id}")
                return {'error': f'Owner not found with ID: {owner_id}'}, 400
            
            print(f"Owner found: {owner.first_name} {owner.last_name}")
            print(f"Owner places before: {owner.places if hasattr(owner, 'places') else 'No places attr'}")
            
            place = Place(**place_data)
            print(f"Place created with ID: {place.id}")
            
            self.place_repo.add(place)
            print(f"Place added to repository")
            
            # Add place to owner's places list
            if hasattr(owner, 'places'):
                owner.places.append(place.id)
                print(f"Added place to owner's places list")
                print(f"Owner places after: {owner.places}")
            else:
                print(f"WARNING: Owner has no 'places' attribute!")
            
            print("=== END DEBUG ===\n")
            
            return place.to_dict(), 201
        except ValueError as e:
            print(f"ValueError in create_place: {str(e)}")
            return {'error': str(e)}, 400
        except Exception as e:
            print(f"Unexpected error in create_place: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': 'Internal server error'}, 500
    
    def get_place(self, place_id):
        """Get place by ID"""
        place = self.place_repo.get(place_id)
        if place:
            # Get owner details
            owner = self.user_repo.get(place.owner_id)
            place_dict = place.to_dict()
            
            # Add owner details
            if owner:
                place_dict['owner'] = {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                }
            
            # Get amenities details
            amenities = []
            for amenity_id in place.amenities:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    amenities.append(amenity.to_dict())
            place_dict['amenities'] = amenities
            
            return place_dict, 200
        return {'error': 'Place not found'}, 404
    
    def get_all_places(self):
        """Get all places"""
        places = []
        for place in self.place_repo.get_all():
            place_dict = place.to_dict()
            # Add owner details
            owner = self.user_repo.get(place.owner_id)
            if owner:
                place_dict['owner'] = {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name
                }
            places.append(place_dict)
        return places, 200
    
    def update_place(self, place_id, place_data):
        """Update place"""
        place = self.place_repo.get(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Don't allow owner_id to be updated
        if 'owner_id' in place_data:
            del place_data['owner_id']
        
        try:
            place.update(place_data)
            return place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
    
    # Review methods
    def create_review(self, review_data):
        """Create a new review with validation"""
        try:
            # Verify user exists
            user = self.user_repo.get(review_data.get('user_id'))
            if not user:
                return {'error': 'User not found'}, 400
            
            # Verify place exists
            place = self.place_repo.get(review_data.get('place_id'))
            if not place:
                return {'error': 'Place not found'}, 400
            
            review = Review(**review_data)
            self.review_repo.add(review)
            
            # Add review to user and place
            user.reviews.append(review.id)
            place.reviews.append(review.id)
            
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def get_review(self, review_id):
        """Get review by ID"""
        review = self.review_repo.get(review_id)
        if review:
            return review.to_dict(), 200
        return {'error': 'Review not found'}, 404
    
    def get_all_reviews(self):
        """Get all reviews"""
        reviews = [review.to_dict() for review in self.review_repo.get_all()]
        return reviews, 200
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a place"""
        place = self.place_repo.get(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        reviews = []
        for review_id in place.reviews:
            review = self.review_repo.get(review_id)
            if review:
                review_dict = review.to_dict()
                # Add user details
                user = self.user_repo.get(review.user_id)
                if user:
                    review_dict['user'] = {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                reviews.append(review_dict)
        
        return reviews, 200
    
    def update_review(self, review_id, review_data):
        """Update review"""
        review = self.review_repo.get(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Don't allow user_id or place_id to be updated
        if 'user_id' in review_data:
            del review_data['user_id']
        if 'place_id' in review_data:
            del review_data['place_id']
        
        try:
            review.update(review_data)
            return review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def delete_review(self, review_id):
        """Delete review"""
        review = self.review_repo.get(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Remove review from user and place
        user = self.user_repo.get(review.user_id)
        if user and review.id in user.reviews:
            user.reviews.remove(review.id)
        
        place = self.place_repo.get(review.place_id)
        if place and review.id in place.reviews:
            place.reviews.remove(review.id)
        
        if self.review_repo.delete(review_id):
            return {'message': 'Review deleted successfully'}, 200
        return {'error': 'Failed to delete review'}, 500
    
    # Amenity methods
    def create_amenity(self, amenity_data):
        """Create a new amenity with validation"""
        try:
            amenity = Amenity(**amenity_data)
            self.amenity_repo.add(amenity)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            return amenity.to_dict(), 200
        return {'error': 'Amenity not found'}, 404
    
    def get_all_amenities(self):
        """Get all amenities"""
        amenities = [amenity.to_dict() for amenity in self.amenity_repo.get_all()]
        return amenities, 200
    
    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        try:
            amenity.update(amenity_data)
            return amenity.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

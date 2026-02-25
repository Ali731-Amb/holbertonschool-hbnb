from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

#---------------------------- User ----------------------

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user_id is None:
            return None
        for key, value in user_data.items():
            setattr(user, key, value)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

#-------------------- Place --------------------------

    def create_place(self, place_data):
    # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        pass

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        pass

#---------------------Amenity-------------------------
def create_amenity(self, amenity_data):
    amenity = Amenity(**amenity_data)
    self.amenity_repo.add(amenity)
    return amenity

def get_amenity(self, amenity_id):
    return self.amenity_repo.get(amenity_id)

def get_all_amenities(self):
    return self.amenity_repo.get_all()

def update_amenity(self, amenity_id, amenity_data):
    amenity = self.amenity_repo.get(amenity_id)
    if amenity:
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
    return amenity

#------------------Reviews--------------------
def create_review(self, review_data):
    review = Review(**review_data)
    self.review_repo.add(review)
    return review

def get_review(self, review_id):
    return self.review_repo.get(review_id)

def get_all_reviews(self):
    return self.review_repo.get_all()

def get_reviews_by_place(self, place_id):
    all_reviews = self.review_repo.get_all()
    return [r for r in all_reviews if r.place_id == place_id]

def update_review(self, review_id, review_data):
    review = self.review_repo.get(review_id)
    if review:
        for key, value in review_data.items():
            setattr(review, key, value)
    return review

def delete_review(self, review_id):
    return self.review_repo.delete(review_id)

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.place import Place

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
        user = self.get_user(user_id)
        for key, value in user_data.items():
            if hasattr(user, key):
                if key == 'password':
                    setattr(user, key, value)
                elif getattr(user, key) != value:
                    setattr(user, key, value)
        user.save()
        self.user_repo.update(user)
        return user

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError (f"User with ID {user_id} not found")
        return user

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

#-------------------- Place --------------------------

    def create_place(self, place_data):
    # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID {owner_id} not found")
        amenities = []
        for aid in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(aid)
            if not amenity:
                raise ValueError(f"Amenity {aid} not found")
            amenities.append(amenity)
        try:
            new_place = Place(
            title=place_data.get('title'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner,
            description=place_data.get('description'),
                            )
            for amenity in amenities:
                new_place.add_amenity(amenity)
            self.place_repo.add(new_place)
            return new_place
        except(ValueError, TypeError) as e: 
            raise ValueError(f"Invalid place data : {e}")


    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} not found")
        return place

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        place = self.get_place(place_id)
        fields_to_update = ['title', 'description', 'price', 'latitude', 'longitude']
        for key in fields_to_update:
            if key in place_data:
                setattr(place, key, place_data[key])
        if 'amenities' in place_data:
            place.amenities = []
            for aid in place_data['amenities']:
                amenity =self.amenity_repo.get(aid)
                if not amenity:
                    raise ValueError(f"Amenity {aid} not found")
                place.add_amenity(amenity)
        self.place_repo.update(place)
        return place


#---------------------Amenity-------------------------
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError(f"Amenity with ID {amenity_id} not found")
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        for key, value in amenity_data.items():
            if hasattr(amenity, key):
                setattr(amenity, key, value)
        amenity.save()
        self.amenity_repo.update(amenity)
        return amenity

#------------------Reviews--------------------
    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        if not user:
            raise ValueError("User not found")
        if not place:
            raise ValueError("Place not found")
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )
        place.add_review(review)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        self.get_place(place_id)
        all_reviews = self.review_repo.get_all()
        return [r for r in all_reviews if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        for key in ['text', 'rating']:
            if key in review_data:
                setattr(review, key, review_data[key])
        self.review_repo.update(review)
        return review

    def delete_review(self, review_id):
        self.get_review(review_id)
        return self.review_repo.delete(review_id)

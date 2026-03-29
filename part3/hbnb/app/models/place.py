from app import db
from .base_model import BaseModel
from .user import User

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.price = kwargs.get('price')
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.user_id = kwargs.get('user_id')


#----------------- Title -----------------
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError("Title must be a string of characters.")
        if len(value) > 100:
            raise ValueError("Title must be under 100 characters")
        self._title = value

#-----------------Description ------------
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("Description must be a string or None")
        self._description = value

#------------------Price -----------------
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("The price must be an integer or a decimal number")
        if value <= 0:
            raise ValueError("The price must be greater than 0.")
        self._price = value

#-----------------Latitude ---------------
    @property
    def latitude(self):
        return self._latitude 
    
    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be an integer or a decimal number")
        if value < -90.0  or value > 90.0 :
            raise ValueError("The latitude must be between -90.0 and 90.0")
        self._latitude = value

#----------------Longitude----------------
    @property
    def longitude(self):
        return self._longitude 
    
    @longitude.setter 
    def longitude(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError("Longitude must be an integer or a decimal number")
        if value < -180.0 or value > 180.0:
            raise ValueError("The longitude must be between -180.0 and 180")
        self._longitude = value

#----------------Owner--------------------
    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("The owner must belong to the user class")
        self._owner = value

#----------------Review------------------
    def add_review(self, review):
        """Add a review to the place"""
        if type(review).__name__ != 'Review':
            raise ValueError("Object must be a Review")
        if review not in self._reviews:
            self._reviews.append(review)


#----------------Amenity------------------
    @property
    def amenities(self):
        return self._amenities 
    
    @amenities.setter
    def amenities(self, value):
        """Add an amenity to the place."""
        if not isinstance(value, list):
            raise ValueError("Amenities must be a list")
        self._amenities = value
    
    def add_amenity(self, amenity):
        """Add an amenity to the place if it's not already present."""
        if type(amenity).__name__ != 'Amenity':
            raise ValueError("The object must be an instance of Amenity")
        if not hasattr(self, '_amenities') or self._amenities is None:
            self._amenities = []
        if amenity not in self._amenities:
            self._amenities.append(amenity)


#---------------------- Dictionnaire ----------------------
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id if self.owner else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            }
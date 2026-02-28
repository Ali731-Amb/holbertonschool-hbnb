from .base_model import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self._reviews = []
        self._amenities = []


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
        """Add a review to the place."""
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
from app import db
from .base_model import BaseModel
from .user import User
from sqlalchemy.orm import validates

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)
class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    # Clé étrangère → un place appartient à un user
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

# Relations
    reviews = db.relationship('Review', backref='place', cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.price = kwargs.get('price')
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.owner_id = kwargs.get('owner_id')


#----------------- Title -----------------
    @validates('title')
    def title(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Title must be a string of characters.")
        if len(value) > 100:
            raise ValueError("Title must be under 100 characters")
        return value

#-----------------Description ------------
    @validates('description')
    def description(self, key, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("Description must be a string or None")
        return value

#------------------Price -----------------
    @validates('price')
    def price(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError("The price must be an integer or a decimal number")
        if value <= 0:
            raise ValueError("The price must be greater than 0.")
        return value

#-----------------Latitude ---------------
    @validates('latitude')
    def latitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be an integer or a decimal number")
        if value < -90.0  or value > 90.0 :
            raise ValueError("The latitude must be between -90.0 and 90.0")
        return value

#----------------Longitude----------------
    @validates('longitude')
    def longitude(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError("Longitude must be an integer or a decimal number")
        if value < -180.0 or value > 180.0:
            raise ValueError("The longitude must be between -180.0 and 180")
        return value

#----------------Owner--------------------
    @validates('owner')
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("The owner must belong to the user class")
        return value

#----------------Review------------------
    def add_review(self, review):
        """Add a review to the place"""
        if type(review).__name__ != 'Review':
            raise ValueError("Object must be a Review")
        if review not in self._reviews:
            self._reviews.append(review)


#----------------Amenity------------------
    @validates('amenity')
    def amenities(self, key, value):
        """Add an amenity to the place."""
        if not isinstance(value, list):
            raise ValueError("Amenities must be a list")
        return value
    
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
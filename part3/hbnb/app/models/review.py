from app import db
from .base_model import BaseModel


class Review(BaseModel):
    __tablename__ = 'reviews'

    content = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = kwargs.get('content')
        self.rating = kwargs.get('rating')
        self.user_id = kwargs.get('user_id')
        self.place_id = kwargs.get('place_id')

# --------------- Text -------------------

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError("Text must be a string of characters")
        if len(value) < 10:
            raise ValueError("Text must be longer than 10 characters")
        self._text = value

# --------------- Rating -----------------
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise ValueError("Rating must be an interger")
        if not 1 <= value <= 5:
            raise ValueError("The grade must be between 1 and 5. ")
        self._rating = value

# --------------- Place ------------------

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        if type(value).__name__ != 'Place':
            raise ValueError("Place must be an instance of Place class")
        self._place = value

# --------------- User -------------------
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if type(value).__name__ != 'User':
            raise ValueError("User must be an instance of User class")
        self._user = value

# ------------------Dictionnaire--------------------
    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place.id,
            "user_id": self.user.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

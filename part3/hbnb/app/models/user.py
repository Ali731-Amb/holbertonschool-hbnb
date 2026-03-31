from .base_model import BaseModel
from app import db
from enum import Enum
from app import bcrypt
import json
from sqlalchemy.orm import validates

# ---------------- Enum Pets ----------------
class PetType(Enum):
    DOG = 1
    CAT = 2
    OTHERS = 3

# ---------------- User ----------------
class User(BaseModel):
    __tablename__ = 'users'

    # Colonnes SQLAlchemy
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    pet = db.Column(db.String(20))  # nom de l'Enum

    places = db.relationship('Place', backref='owner', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.is_admin = kwargs.get('is_admin', False)

        pet_value = kwargs.get('pet')
        self._pet = None
        if pet_value:
            self.pets = pet_value

    # ----------------First name ----------------

    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("First name cannot be empty")
        if len(value) > 50:
            raise ValueError("First name must be under 50 characters")
        return value

    # ---------------Last Name -----------------
    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Last name cannot be empty")
        if len(value) > 50:
            raise ValueError("Last name must be under 50 characters")
        return value

    # --------------------- Email -----------------
    @validates('email')
    def email(self, key, value):
        value = User.validate_email(value)

    @staticmethod
    def validate_email(email):
        parts = email.split('@')
        if len(parts) != 2:
            raise ValueError("Email invalide")
        if not email.endswith(".com") and not email.endswith(".fr"):
            raise ValueError("Email invalide")
        if parts[0] == "" or parts[1] == "" or parts[1][0] == ".":
            raise ValueError("Email invalide")
        return email

    # ------------------- Password ----------------------------
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, value):
        validated_password = User.validate_password(value)
        self._password = bcrypt.generate_password_hash(
            validated_password).decode('utf-8')

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        has_digit = False
        has_upper = False
        for char in password:
            if char.isupper():
                has_upper = True
            if char.isdigit():
                has_digit = True
        if not has_upper:
            raise ValueError("A capital letter is missing ")
        if not has_digit:
            raise ValueError("A number is missing")
        return password

    def verify_password(self, password_to_check):
        """Check password"""
        return bcrypt.check_password_hash(self._password, password_to_check)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # ------------------------ Admin ------------------------------
    @validates('is_admin')
    def is_admin(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        return value

    # -----------------Pets-------------------------
    @property
    def pets(self):
        return self._pets

    @pets.setter
    def pets(self, value):
        if value is None:
            self._pets = None
        elif isinstance(value, PetType):
            self._pets = value
        elif isinstance(value, str):
            try:
                self._pets = PetType[value.upper()]
            except KeyError:
                raise ValueError(f"'{value}' is not valid animal.")
        else:
            raise ValueError("Format animal invalide.")
        self.__dict__['pet'] = self._pets.name if self._pets else None

    # --------------------Dictionnaire------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "Pets": self.pets.name if self.pets else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

from app import db
from .base_model import BaseModel
from sqlalchemy.orm import validates

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')

    @validates('name')
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Amenity name must be a string")
        if not value.strip():
            raise ValueError("Amenity name cannot be empty")
        if len(value) > 50:
            raise ValueError("Amenity name must be under 50 characters")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

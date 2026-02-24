from .base_model import BaseModel

class Amenity(BaseModel):
	def __init__(self, name):
		super().__init__()
		self.name = name

	@property
	def name(self):
		return self._name
	
	@name.setter
	def name(self, value):
		if not isinstance(value, str):
			raise ValueError("Amenity name must be a string")
		if len(value) > 50:
			raise ValueError("Amenity name must be under 50 characters")
		self._name = value

from .base_model import BaseModel

class Review(BaseModel):
	def __init__(self, text, rating, place, user, **kwargs):
		super().__init__(**kwargs)
		self.text = text 
		self.rating = rating 
		self.place = place
		self.user = user 

#--------------- Text -------------------

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

#--------------- Rating -----------------
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

		

#--------------- Place ------------------
	@property
	def place(self):
		return self._place
	
	@place.setter
	def place(self, value):
		if not isinstance(value, str):
			raise ValueError("Place must be a string of characters")
		self._place = value

#--------------- User -------------------
	@property
	def user(self):
		return self._user
	
	@user.setter
	def user(self, value):
		if not isinstance(value, str):
			raise ValueError("User must be a string of characters")
		self._user = value

#------------------Dictionnaire--------------------
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

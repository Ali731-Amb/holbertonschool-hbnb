from .base_model import BaseModel
from werkzeug.security import generate_password_hash
from enum import Enum

class PetType(Enum):
		DOG = 1
		CAT = 2 
		OTHERS = 3


class User(BaseModel):
	def __init__(self, first_name, last_name, email, password = None, is_admin = False, pets = None):
		super().__init__()
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.is_admin = is_admin
		self.password = password if password else "Default123"
		self.pets = pets

#----------------First name ----------------
	@property
	def first_name(self):
		return self._first_name

	@first_name.setter
	def first_name(self, value):
		if len(value) > 50:
			raise ValueError("First name must be under 50 characters")
		self._first_name = value

#---------------Last Name -----------------
	@property
	def last_name(self):
		return self._last_name
	
	@last_name.setter
	def last_name(self, value):
		if len(value) > 50:
			raise ValueError("Last name must be under 50 characters")
		self._last_name = value 

#--------------------- Email -----------------

	@property
	def email(self):
		return self._email
	
	@email.setter 
	def email(self, value):
		self._email = User.validate_email(value)

	@staticmethod
	def validate_email(email):
		parts = email.split('@')
		if len(parts) != 2:
			raise ValueError("Email invalide")
		if not email.endswith(".com") and not email.endswith(".fr"):
			raise ValueError("Email invalide")
		if parts[0] =="" or parts [1] == "" or parts[1][0] ==".":
			raise ValueError("Email invalide")
		return email

#------------------- Password ----------------------------
	@property
	def password(self):
		raise AttributeError("Password is not a readable attribute")

	@password.setter
	def password(self, value):
		self._password = User.validate_password(value)

	@staticmethod
	def validate_password(password):
		if len(password) < 8:
			raise ValueError("Password invalide")
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
		return generate_password_hash(password)

#------------------------ Admin ------------------------------
	@property
	def is_admin(self):
		return self._is_admin
	
	@is_admin.setter
	def is_admin(self, value):
		if not isinstance(value, bool):
			raise ValueError("is_admin must be a boolean")
		self._is_admin = value

#-----------------Pets-------------------------
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

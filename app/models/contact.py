from orm import model
from orm import fields
from .user import User

class Contact(model.Model):
	name = fields.CharField(max_length=400)
	owner = fields.ForeignKeyField(User)
	address = fields.CharField(max_length=400, blank=True)
	zip_code = fields.CharField(max_length=40, blank=True)
	city = fields.CharField(max_length=100, blank=True)
	email = fields.CharField(max_length=200, blank=True)
	
	def __repr__(self):
		return self.name
from orm import model
from .user import User
from orm import fields

class Account(model.Model):
	name = fields.CharField(max_length=40)
	aid = fields.IntegerField()
	owner = fields.ForeignKeyField(User, blank=True)
	description = fields.CharField(max_length=400, blank=True)
	side = fields.CharField(max_length=13)

	def __repr__(self):
		return str(self.pk)+": "+self.name
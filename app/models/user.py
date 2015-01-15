from orm import models
from orm import fields

class User(models.Model):
	first_name = fields.CharField(max_length=40)
	last_name = fields.CharField(max_length=40)
	username = fields.CharField(max_length=40)
	password = fields.CharField(max_length=40)

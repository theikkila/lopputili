from orm import models
from orm import fields

class Account(models.Model):
	name = fields.CharField(max_length=40)
	aid = fields.IntegerField()
	description = fields.CharField(max_length=400, blank=True)
	side = fields.CharField(max_length=13)

from orm import model
from .user import User
from .account import Account
from orm import fields

class Receipt(model.Model):
	rid = fields.IntegerField()
	owner = fields.ForeignKeyField(User)
	commits = fields.HasField('Commit', 'receipt')
	commit_date = fields.DateTimeField()
	description = fields.CharField(max_length=400, blank=True)

	def __repr__(self):
		return str(self.rid)

class Commit(model.Model):
	owner = fields.ForeignKeyField(User)
	receipt = fields.ForeignKeyField(Receipt)
	account = fields.ForeignKeyField(Account)
	credit_amount = fields.IntegerField()
	debet_amount = fields.IntegerField()

	def __repr__(self):
		return self.receipt
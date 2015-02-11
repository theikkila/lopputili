from orm import model
from orm import fields
import bcrypt

class User(model.Model):
	first_name = fields.CharField(max_length=40, blank=True)
	last_name = fields.CharField(max_length=40, blank=True)
	username = fields.CharField(max_length=100)
	password = fields.CharField(max_length=100)

	def is_valid_password(self, pw2):
		return bcrypt.hashpw(pw2.encode('utf-8'), self.password) == self.password

	def set_password(self, passwd):
		self.password = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
		return self
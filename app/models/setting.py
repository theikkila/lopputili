from orm import model
from .user import User
from orm import fields

class Setting(model.Model):
	owner = fields.ForeignKeyField(User)
	company_name = fields.CharField(max_length=140, blank=True)
	address = fields.CharField(max_length=240, blank=True)
	zip_code = fields.CharField(max_length=140, blank=True)
	city = fields.CharField(max_length=140, blank=True)
	phone = fields.CharField(max_length=140, blank=True)
	email = fields.CharField(max_length=140, blank=True)
	vat_code = fields.CharField(max_length=140, blank=True)
	iban = fields.CharField(max_length=140, blank=True)
	bic = fields.CharField(max_length=140, blank=True)

	def __repr__(self):
		return str(self.company_name)
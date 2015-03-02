from orm import model
from orm import fields
from .contact import Contact
from .user import User

class Invoice(model.Model):
	title = fields.CharField(max_length=200)
	owner = fields.ForeignKeyField(User)
	description = fields.CharField(max_length=400, blank=True)
	contact = fields.ForeignKeyField(Contact, blank=True)
	created = fields.DateTimeField()
	invoice_id = fields.IntegerField()
	ref = fields.CharField(max_length=200)
	our_ref = fields.CharField(max_length=200, blank=True)
	your_ref = fields.CharField(max_length=200, blank=True)
	payment_type = fields.CharField(max_length=200)
	due_date = fields.DateField()
	reclamation_time = fields.IntegerField()
	penalty_interest = fields.DecimalField()
	info1 = fields.CharField(max_length=200, blank=True)
	info2 = fields.CharField(max_length=200, blank=True)
	status = fields.CharField(max_length=40)
	products = fields.HasField('Product', 'invoice')

	def __repr__(self):
		return str(self.title)

class Product(model.Model):
	owner = fields.ForeignKeyField(User)
	invoice = fields.ForeignKeyField(Invoice)
	name = fields.CharField(max_length=200)
	price = fields.IntegerField()
	count = fields.IntegerField()
	discount = fields.IntegerField()
	vat = fields.IntegerField()

	def __repr__(self):
		return str(self.name)

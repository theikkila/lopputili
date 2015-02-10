from orm import model
from orm import fields
from .contact import Contact

class Invoice(model.Model):
	title = fields.CharField(max_length=200)
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
	summ = fields.DecimalField()
	info1 = fields.CharField(max_length=200, blank=True)
	info2 = fields.CharField(max_length=200, blank=True)

	def __repr__(self):
		return self.title
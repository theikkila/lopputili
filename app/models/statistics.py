from orm import model
from orm import fields

class Visit(model.Model):
	useragent = fields.CharField(max_length=400)
	time = fields.DateTimeField()

	def __repr__(self):
		return str(self.pk)+": "+self.name
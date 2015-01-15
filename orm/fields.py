

class Field(object):
	def __init__(self, blank=False):
		self.meta = {}
		self.blank = blank
		self.value = None

	def get(self):
		return self.value

	def set(self, value):
		self.value = value

	def isvalid(self):
		if not self.blank and self.value is None:
			return False
		return True

	def __repr__(self):
		return str(self.value)

class PKField(Field):
	name = "PrimaryKey"

class DateTimeField(Field):
	name = "DateTimeField"

class CharField(Field):
	name = "String"
	def __init__(self, max_length=30, blank=False):
		super(CharField, self).__init__(blank=blank)
		self.meta['max_length'] = max_length


class IntegerField(Field):
	name = "Integer"
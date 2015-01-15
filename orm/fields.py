

class Field(object):
	def __init__(self, blank=False):
		self.meta = {}
		self.blank = blank

class AutoField(Field):
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
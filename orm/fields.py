

class Field(object):
	def __init__(self):
		self.meta = {}

class AutoField(Field):
	name = "PrimaryKey"

class DateTimeField(Field):
	name = "DateTimeField"

class CharField(Field):
	name = "String"
	def __init__(self, max_length=30):
		super(CharField, self).__init__()
		self.meta['max_length'] = max_length


class IntegerField(Field):
	name = "Integer"
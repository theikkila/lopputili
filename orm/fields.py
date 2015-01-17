from weakref import WeakKeyDictionary


class FieldDescriptor(object):
	def __init__(self, attrib):
		self.test = {}
		self.attrib = attrib

	def __get__(self, instance=None, owner=None):
		return getattr(instance, '_'+self.attrib).value

	def __set__(self, instance, value):
		getattr(instance, '_'+self.attrib).value = value

class Field(object):
	def __init__(self, blank=False):
		self.meta = {}
		self.blank = blank
		self.value = None

	def isvalid(self):
		if not self.blank and self.value is None:
			return False
		return True

class PKField(Field):
	name = "PrimaryKey"

	def isvalid(self):
		return True

class DateTimeField(Field):
	name = "DateTimeField"

class CharField(Field):
	name = "String"
	def __init__(self, max_length=30, blank=False):
		super(CharField, self).__init__(blank=blank)
		self.meta['max_length'] = max_length

	def isvalid(self):
		if not super(CharField, self).isvalid():
			return False
		return len(str(self.value)) <= self.meta['max_length']

class IntegerField(Field):
	name = "Integer"

	def isvalid(self):
		if not super(IntegerField, self).isvalid():
			return False
		return isinstance(self.value, int)
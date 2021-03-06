from weakref import WeakKeyDictionary

from datetime import datetime, date

class Field(object):
	def __init__(self, blank=False):
		self.meta = {}
		self.blank = blank
		self.value = None

	def isvalid(self):
		if not self.blank and self.value is None:
			return False
		return True

	def serialize(self):
		return self.value

	def deserialize(self, value):
		self.value = value

class MetaField(object):
	def __init__(self):
		self.meta = {}
		self.value = None

	def isvalid(self):
		return True

class ForeignKeyField(Field):
	name = "ForeignKey"
	def __init__(self, model, blank=False):
		super(ForeignKeyField, self).__init__(blank=blank)
		self.meta['model'] = model
		self.meta['tablename'] = model.tableName()

		self.value = None
		self.instance = None

	def create(self, *args, **kwargs):
		self.instance = self.meta['model'](*args, **kwargs)


class HasField(MetaField):
	name = "HasField"
	def __init__(self, modelclass, field):
		super(HasField, self).__init__()
		from . import model
		if isinstance(modelclass, model.BaseModel):
			self.meta['model_name'] = modelclass.__name__
			self.meta['model'] = modelclass
		else:
			self.meta['model_name'] = modelclass
		self.meta['field'] = field

	def setModel(self, instance):
		self.meta['instance'] = instance
		if self.meta.get('model', None) is None:
			self.meta['model'] = self.meta['instance'].orm.nmodels[self.meta['model_name']]

	def all(self):
		kw = {}
		kw[self.meta['field']+'__exact'] = self.meta['instance'].pk
		return self.meta['model'].filter(**kw)

	def deserialize(self, oblist):
		return
		# Todo: fix this
		inst = self.meta['instance']
		for obj in oblist:
			obj[self.meta['field']] = inst.pk
			obj['owner'] = inst.owner
			m = self.meta['model'].deserialize(obj)
			m.save()


class PKField(Field):
	name = "PrimaryKey"

	def isvalid(self):
		return True

class DateTimeField(Field):
	name = "DateTimeField"

	def deserialize(self, value):
		if isinstance(value, datetime):
			self.value = value
		else:
			try:
				self.value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
			except ValueError:
				self.value = datetime()

	def serialize(self):
		return self.value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

	def isvalid(self):
		if not super(DateTimeField, self).isvalid():
			return False
		try:
			v = datetime.strptime(self.value, '%Y-%m-%dT%H:%M:%S.%fZ')
		except ValueError:
			return False
		except TypeError:
			pass
		return isinstance(self.value, datetime)

class DateField(Field):
	name = "DateField"

	def deserialize(self, value):
		if isinstance(value, datetime):
			self.value = value
		else:
			self.value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')

	def serialize(self):
		return self.value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

	def isvalid(self):
		if not super(DateField, self).isvalid():
			return False
		return isinstance(self.value, date)

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

class DecimalField(Field):
	name = "Decimal"

	def isvalid(self):
		if not super(DecimalField, self).isvalid():
			return False
		return isinstance(self.value, float) or isinstance(self.value, int)


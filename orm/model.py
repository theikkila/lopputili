from . import fields
import inspect
from .query import queryset
from . import exceptions
from . import collections
import datetime

from . import modelmeta
BaseMetaModel = modelmeta.BaseMetaModel

def dbset(model):
	if model.db is None:
		raise exceptions.ModelNotRegisteredError		


class BaseModel(BaseMetaModel):
	db = None
	conn = None
	def __init__(self, insert=True, **kwargs):
		super(BaseModel, self).__init__()
		self.insert = insert
		for key in kwargs:
			if key in self.fields:
				setattr(self, key, kwargs[key])

	def serialize(self):
		d = {}
		for field_name in self.getfields():
			field = getattr(self, '_'+field_name)
			if not field.isvalid():
				print("Error @", field_name)
				raise exceptions.FieldNotValidError(field_name)
			d[field_name] = field.serialize()
		return d

	@classmethod
	def deserialize(model, raw, insert=False):
		a = model()
		for field in raw:
			getattr(a, '_'+field).deserialize(raw[field])
		a.insert = insert
		return a

	def save(self):
		dbset(self)
		serialized = self.serialize()
		if self.insert:
			self.insert = False
			self.pk = self.db.insert(self.tableName(), serialized)
		else:
			self.db.update(self.tableName(), serialized)
		return self

	def delete(self):
		dbset(self)
		print(self.db.delete(self.tableName(), self.pk))
		return self

	@classmethod
	def get(model, pk):
		dbset(model)
		fetched = model.db.getById(model.tableName(), pk)
		if fetched is None:
			raise exceptions.ObjectNotFoundError()
		return model.deserialize(fetched)

	@classmethod
	def filter(model, *args, **kwargs):
		dbset(model)
		query = queryset(*args, **kwargs)
		res = model.db.filter(model.tableName(), query)
		coll = []
		for item in res:
			coll.append(model.deserialize(item))
		return collections.ModelCollection(coll)

	@classmethod
	def all(model):
		dbset(model)
		res = model.db.all(model.tableName())
		collection = []
		for item in res:
			collection.append(model.deserialize(item))
		return collections.ModelCollection(collection)

	@classmethod
	def setDB(cls, db, orm):
		cls.db = db
		cls.orm = orm

	@classmethod
	def tableName(cls):
		if hasattr(cls, "table"):
			return cls.table
		else:
			return cls.__name__.lower()+"s"

	@classmethod
	def getfields(model):
		#field_names = [field for field in dir(model) if isinstance(getattr(model, field), fields.Field)]
		#field_names = map(lambda field: field[1:], field_names)
		return model.fields

	@classmethod
	def fieldtype(model, field):
		return getattr(model, '_'+field).__class__.__name__

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		else:
			return False

class Model(BaseModel):
	#updated = fields.DateTimeField()
	#created = fields.DateTimeField()
	pass
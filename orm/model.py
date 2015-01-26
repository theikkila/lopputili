from . import fields
import inspect
from .query import queryset
from . import exceptions
from . import collections
import datetime
import copy

def dbset(model):
	if model.db is None:
		raise exceptions.ModelNotRegisteredError		

class ModelMeta(type):
	def __new__(cls, name, based, attributes):
		#print ("Metaclass called")
		if 'pk' not in attributes:
			attributes['pk'] = fields.PKField()
		new_attributes = {}
		new_attributes['fields'] = []
		for attrib_name in attributes:
			attribute = attributes[attrib_name]
			if isinstance(attribute, fields.Field):
				new_attributes['fields'].append(attrib_name)
				#print(new_attributes['fields'])
				new_attributes['_'+attrib_name] = attribute
				new_attributes[attrib_name] = fields.FieldDescriptor(attrib_name)
			else:
				new_attributes[attrib_name] = attribute
		return super(ModelMeta, cls).__new__(cls, name, based, new_attributes)

class BaseMetaModel(object, metaclass=ModelMeta):
	def __init__(self, *args, **kwargs):
		for field in self.fields:
			#print field
			setattr(self, '_'+field, copy.deepcopy(getattr(self, '_'+field)))
			f = getattr(self, '_'+field)
			#print(f, "on", '_'+field)
			#setattr(self, field, fields.FieldDescriptor('_'+field, f))

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
			d[field_name] = field.value
		return d

	@classmethod
	def deserialize(model, row):
		a = model()
		for field in row:
			getattr(a, '_'+field).value = row[field]
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
	def setDB(cls, db):
		cls.db = db

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



class Model(BaseModel):
	#updated = fields.DateTimeField()
	#created = fields.DateTimeField()
	pass
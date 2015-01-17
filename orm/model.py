from . import fields
import inspect
from . import dbwords
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
		del serialized['pk']
		keys = ', '.join(list(serialized.keys()))
		updatepairs = ', '.join([key+" = ?" for key in list(serialized.keys())])
		qmarks = ', '.join('?' * len(serialized))
		cursor = self.conn.cursor()
		if self.insert:
			query = "INSERT INTO %s (%s) VALUES (%s)" % (self.tableName(), keys, qmarks)
			self.insert = False
			res = cursor.execute(query, list(serialized.values()))
		else:
			query = "UPDATE %s SET %s WHERE pk = ?" % (self.tableName(), updatepairs)
			res = cursor.execute(query, list(serialized.values())+[self.pk])
		self.conn.commit()
		if cursor.lastrowid != None:
			self.pk = cursor.lastrowid

	@classmethod
	def get(model, pk):
		dbset(model)
		cursor = model.conn.cursor()
		query = "SELECT * FROM %s WHERE pk = ?" % model.tableName()
		res = cursor.execute(query, (pk,))
		fetched = res.fetchone()
		if fetched is None:
			raise exceptions.ObjectNotFoundError()
		return model.deserialize(fetched)

	@classmethod
	def filter(model, query):
		dbset(model)
		cursor = model.conn.cursor()
		base_query = "SELECT * FROM %s WHERE " % model.tableName()
		values = []
		sql_parts = []
		for sqlpart, value in query.sqls(dbwords.curryOperator(model.db)):
			values.append(value)
			sql_parts.append(sqlpart)
		query = base_query + " AND ".join(sql_parts)
		res = cursor.execute(query, values)
		coll = []
		for item in res:
			coll.append(model.deserialize(item))
		return collections.ModelCollection(coll)

	@classmethod
	def all(model):
		dbset(model)
		cursor = model.conn.cursor()
		res = cursor.execute("SELECT * FROM %s" % model.tableName())
		collection = []
		for item in res:
			collection.append(model.deserialize(item))
		return collections.ModelCollection(collection)

	@classmethod
	def setDB(cls, db, conn):
		cls.db = db
		cls.conn = conn

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


	@classmethod
	def createTableSQL(model):
		dbset(model)
		field_names = model.getfields()
		fields = []
		for field_name in field_names:
			f = getattr(model, '_'+field_name)
			ft = model.fieldtype(field_name)
			sqtype = dbwords.gettype(model.db, ft) % getattr(model, '_'+field_name).meta
			field = field_name + " " + sqtype
			fields.append(field)
		#print ", ".join(fields)
		return 'CREATE TABLE {table} ({fields})'.format(table=model.tableName(), fields=", ".join(fields))

	@classmethod
	def createTables(model):
		dbset(model)
		cursor = model.conn.cursor()
		cursor.execute(model.createTableSQL())


class Model(BaseModel):
	#updated = fields.DateTimeField()
	#created = fields.DateTimeField()
	pass
import fields
import inspect
import orm
import dbwords
import exceptions
import datetime

def dbset(model):
	if model.db is None:
		raise exceptions.ModelNotRegisteredError		

# method factory for an attribute get method
def getmethod(attrname):
    def _getmethod(self):
        return getattr(self, "_"+attrname).get()
    return _getmethod

def setmethod(attrname):
    def _setmethod(self, value):
        return getattr(self, "_"+attrname).set(value)
    return _setmethod

class ModelMeta(type):
    def __new__(cls, name, parents, dct):
    	ccd = {}
    	ccd['fields'] = []
    	for field in dct:
    		if isinstance(dct[field], fields.Field):
    			ccd['fields'].append(field)
    			ccd['_'+field] = dct[field]
    			#  dct['_'+field].set, dct['_'+field].del
    			ccd[field] = property(getmethod(field), setmethod(field))
    		else:
    			ccd[field] = dct[field]
    	#print ccd
    	return super(ModelMeta, cls).__new__(cls, name, parents, ccd)

class BaseModel:
	__metaclass__ = ModelMeta
	db = None
	conn = None
	pk = fields.AutoField()
	def __init__(self, insert=True):
		self.pk = fields.AutoField()
		self.insert = insert

	def serialize(self):
		d = {}
		for field in self.getfields():
			d[field] = getattr(self, field)

	@classmethod
	def deserialize(model, row):
		a = model()
		for field in row:
			getattr(a, '_'+field).set(row[field])
		return a

	def save(self):
		dbset(self)
		serialized = self.serialize()
		keys = ', '.join(serialized.keys())
		qmarks = ', '.join('?' * len(serialized))
		cursor = self.conn.cursor()
		if self.insert:
			query = "INSERT INTO %s (%s) VALUES (%s)" % (self.tableName(), keys, qmarks)
			#print query, serialized.values(), self.pk
			cursor.execute(query, serialized.values())
		else:
			query = "UPDATE %s SET (%s) VALUES (%s) WHERE pk = ?" % (qmarks, qmarks)
			#print query
			cursor.execute(query, serialized.keys()+serialized.values(), self.pk)
		self.conn.commit()

	@classmethod
	def all(model):
		dbset(model)
		cursor = model.conn.cursor()
		res = cursor.execute("SELECT * FROM %s" % model.tableName())
		collection = []
		for item in res:
			collection.append(model.deserialize(item))
		return collection

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
		field_names = [field for field in dir(model) if isinstance(getattr(model, field), fields.Field)]
		field_names = map(lambda field: field[1:], field_names)
		return field_names

	@classmethod
	def fieldtype(model, field):
		return getattr(model, '_'+field).__class__.__name__


	@classmethod
	def createTableSQL(model):
		dbset(model)
		field_names = model.getfields()
		fields = []
		for field_name in field_names:
			f = getattr(model, field_name)
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
	updated = fields.DateTimeField()
	created = fields.DateTimeField()
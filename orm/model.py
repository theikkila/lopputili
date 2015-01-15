import fields
import inspect
import orm
import dbwords
import exceptions

		

class BaseModel:
	db = None
	cursor = None

	def __init__(self):
		pass

	def serialize(self):
		pass
	def deserialize(self):
		pass

	@classmethod
	def setDB(cls, db, cursor):
		cls.db = db
		cls.cursor = cursor

	@classmethod
	def tableName(cls):
		if hasattr(cls, "table"):
			return cls.table
		else:
			return cls.__name__.lower()+"s"

	@classmethod
	def getfields(model):
		return [key for key in dir(model) if isinstance(getattr(model, key), fields.Field)]

	@classmethod
	def fieldtype(model, field):
		return getattr(model, field).__class__.__name__


	@classmethod
	def createTableSQL(model):
		if model.db is None:
			raise exceptions.ModelNotRegisteredError
		field_names = model.getfields()
		fields = []
		for field_name in field_names:
			f = getattr(model, field_name)
			ft = model.fieldtype(field_name)
			sqtype = dbwords.gettype(model.db, ft) % getattr(model, field_name).meta
			field = field_name + " " + sqtype
			fields.append(field)
		return 'CREATE TABLE {table} ({fields})'.format(table=model.tableName(), fields=", ".join(fields))

	@classmethod
	def createTables(model):
		if model.db is None:
			raise exceptions.ModelNotRegisteredError
		model.cursor.execute(model.createTableSQL())


class Model(BaseModel):
	pk = fields.AutoField()
	updated = fields.DateTimeField()
	created = fields.DateTimeField()
import fields
import inspect


class BaseModel:
	def __init__(self):
		pass

	def serialize(self):
		pass
	def deserialize(self):
		pass

	@classmethod
	def tableName(cls):
		if hasattr(cls, "table"):
			return cls.table
		else:
			return cls.__name__.lower()+"s"

class Model(BaseModel):
	pk = fields.AutoField()
	updated = fields.DateTimeField()
	created = fields.DateTimeField()
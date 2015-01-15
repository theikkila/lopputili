import fields
import inspect


class BaseModel:
	def __init__(self):
		pass

	def serialize(self):
		pass
	def deserialize(self):
		pass
	def tableName(self):
		if hasattr(self, "table"):
			return self.table
		else:
			return self.__class__.__name__.lower()+"s"

class Model(BaseModel):
	pk = fields.AutoField()
	updated = fields.DateTimeField()
	created = fields.DateTimeField()
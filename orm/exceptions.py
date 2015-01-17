

class ModelNotRegisteredError(Exception):
	pass

class FieldNotValidError(Exception):
	def __init__(self, field):
		self.field = field

class ObjectNotFoundError(Exception): pass
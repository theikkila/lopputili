


class FieldDescriptor(object):
	def __init__(self, attrib):
		self.test = {}
		self.attrib = attrib

	def __get__(self, instance=None, owner=None):
		return getattr(instance, '_'+self.attrib).value

	def __set__(self, instance, value):
		getattr(instance, '_'+self.attrib).value = value

class HasFieldDescriptor(object):
	def __init__(self, attrib_name):
		self.attrib = attrib_name
		self.cached = None

	def __get__(self, instance=None, owner=None):
		#if self.cached:
		#	return self.cached
		at = getattr(instance, '_'+self.attrib)
		self.cached = at.all()
		return self.cached

	def __set__(self, instance, value):
		#at = getattr(instance, '_'+self.attrib)
		pass
		
class ForeignFieldDescriptor(object):
	def __init__(self, attrib):
		self.test = {}
		self.attrib = attrib

	def __get__(self, instance=None, owner=None):
		at = getattr(instance, '_'+self.attrib)
		if at.instance is None and at.value is not None:
			# Getting model instance from DB
			inst = at.meta['model'].get(at.value)
			at.instance = inst
			return at.instance
		elif at.instance is not None:
			# Returning already defined instance
			return at.instance
		else:
			return None

	def __set__(self, instance, value):
		from . import model
		at = getattr(instance, '_'+self.attrib)
		if isinstance(value, model.BaseModel):
			at.instance = value
			at.value = value.pk
		else:
			at.instance = None
			at.value = value
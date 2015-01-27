from . import fields
from . import descriptors
import copy

class ModelMeta(type):
	def __new__(cls, name, based, attributes):
		#print ("Metaclass called")
		if 'pk' not in attributes:
			attributes['pk'] = fields.PKField()
		new_attributes = {}
		new_attributes['fields'] = []
		new_attributes['metafields'] = []
		for attrib_name in attributes:
			attribute = attributes[attrib_name]
			if isinstance(attribute, fields.Field):
				new_attributes['fields'].append(attrib_name)
				new_attributes['_'+attrib_name] = attribute
				if isinstance(attribute, fields.ForeignKeyField):
					new_attributes[attrib_name] = descriptors.ForeignFieldDescriptor(attrib_name)
				else:
					new_attributes[attrib_name] = descriptors.FieldDescriptor(attrib_name)
			elif isinstance(attribute, fields.MetaField):
				new_attributes['metafields'].append(attrib_name)
				new_attributes['_'+attrib_name] = attribute
				new_attributes[attrib_name] = descriptors.HasFieldDescriptor(attrib_name)
			else:
				new_attributes[attrib_name] = attribute
		return super(ModelMeta, cls).__new__(cls, name, based, new_attributes)

class BaseMetaModel(object, metaclass=ModelMeta):
	def __init__(self, *args, **kwargs):
		for field in self.fields:
			setattr(self, '_'+field, copy.deepcopy(getattr(self, '_'+field)))
		for metafield in self.metafields:
			setattr(self, '_'+metafield, copy.copy(getattr(self, '_'+metafield)))
			f = getattr(self, '_'+metafield)
			f.setModel(self)



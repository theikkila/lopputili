from . import fields
from . import descriptors
import copy

'''
This is the most magical part of the orm.
Metaclass constructs other classes.
In practice converts Models from nice declarative format into working ones.
'''

class ModelMeta(type):
	def __new__(cls, name, based, attributes):
		#print ("Metaclass called")
		# Always add primary key field
		if 'pk' not in attributes:
			attributes['pk'] = fields.PKField()
		new_attributes = {}
		new_attributes['fields'] = []
		new_attributes['metafields'] = []
		# Iterate through attributes (model fields)
		for attrib_name in attributes:
			attribute = attributes[attrib_name]
			if isinstance(attribute, fields.Field):
				new_attributes['fields'].append(attrib_name)
				new_attributes['_'+attrib_name] = attribute
				# This assigns descriptor to fields place and moves the original field class to _field-attribute
				if isinstance(attribute, fields.ForeignKeyField):
					new_attributes[attrib_name] = descriptors.ForeignFieldDescriptor(attrib_name)
				else:
					new_attributes[attrib_name] = descriptors.FieldDescriptor(attrib_name)
			elif isinstance(attribute, fields.MetaField):
				# Metafields like related-objects are not real fields so they are handled differently
				new_attributes['metafields'].append(attrib_name)
				new_attributes['_'+attrib_name] = attribute
				new_attributes[attrib_name] = descriptors.HasFieldDescriptor(attrib_name)
			else:
				new_attributes[attrib_name] = attribute
		return super(ModelMeta, cls).__new__(cls, name, based, new_attributes)


'''
This class is contructed by metaclass and in its contructor all the class contructors
are copied so the instances wouldn't be only references to each other.
'''
class BaseMetaModel(object, metaclass=ModelMeta):
	def __init__(self, *args, **kwargs):
		for field in self.fields:
			setattr(self, '_'+field, copy.deepcopy(getattr(self, '_'+field)))
		for metafield in self.metafields:
			setattr(self, '_'+metafield, copy.copy(getattr(self, '_'+metafield)))
			f = getattr(self, '_'+metafield)
			f.setModel(self)



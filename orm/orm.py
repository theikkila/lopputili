import fields


def getfields(model):
	return [key for key in dir(model) if isinstance(getattr(model, key), fields.Field)]

def fieldtype(field, model):
	return getattr(model, field).__class__.__name__
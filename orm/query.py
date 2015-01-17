

def exact(model, field, value):
	return getattr(model, field) == value

def iexact(model, field, value):
	return str(getattr(model, field)).upper() == str(value).upper()

def contains(model, field, value):
	return str(value) in str(getattr(model, field))

def icontains(model, field, value):
	return str(value).upper() in str(getattr(model, field)).upper()

def gt(model, field, value):
	return getattr(model, field) > value

def gte(model, field, value):
	return getattr(model, field) >= value

def lt(model, field, value):
	return getattr(model, field) < value

def lte(model, field, value):
	return getattr(model, field) <= value


operators_filters = {
    'exact': exact,
    'iexact': iexact,
    'contains': contains,
    'icontains': icontains,
    'gt': gt,
    'gte': gte,
    'lt': lt,
    'lte': lte
}


class Query(object):
	def __init__(self, **kwargs):
		self.params = []
		if kwargs is not None:
			for key in kwargs:
				field, operator = key.split('__')
				self.params.append((field, operator, kwargs[key]))
	
	def sqls(self, oper):
		for param in self.params:
			field, o, value = param
			statement = field + " " + oper(o) % '?'	
			yield (statement, value)

	def filt(self, item):
		for field, operator, value in self.params:
			if not operators_filters[operator](item, field, value):
				return False
		return True
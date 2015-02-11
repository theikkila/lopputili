from .query import Query, queryset

class ModelCollection(object):
	"""Implements model collection with behavior like arrays + utility functions and filtering"""
	def __init__(self, arr):
		self.arr = arr

	def __getitem__(self, index):
		return self.arr[index]

	def __setitem__(self, index, value):
		self.arr[index] = value

	def __iter__(self):
		return iter(self.arr)

	def __len__(self):
		return len(self.arr)

	def filter(self, *args, **kwargs):
		q = queryset(*args, **kwargs)
		return ModelCollection([item for item in iter(self.arr) if q.filt(item)])

	def serialize(self):
		def seri(x): return x.serialize()
		return list(map(seri, self.arr))

	def __repr__(self):
		return str(self.arr)
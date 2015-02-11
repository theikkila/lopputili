from .listview import APIListView, APIDetailView
from ..models.receipt import Receipt, Commit

class ReceiptsListController(APIListView):

	def getModel(self):
		return Receipt

class ReceiptsDetailController(APIDetailView):

	def getModel(self):
		return Receipt


class CommitsListController(APIListView):

	def getModel(self):
		return Commit

class CommitsDetailController(APIDetailView):

	def getModel(self):
		return Commit
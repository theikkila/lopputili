from .listview import APIListView, APIDetailView
from .login import api_login_required
from ..models.receipt import Receipt, Commit

class ReceiptsListController(APIListView):
	methods = ['GET', 'POST']
	decorators = [api_login_required]

	def getModel(self):
		return Receipt

class ReceiptsDetailController(APIDetailView):
	methods = ['GET', 'PUT', 'DELETE']
	decorators = [api_login_required]

	def getModel(self):
		return Receipt


class CommitsListController(APIListView):
	methods = ['GET', 'POST']
	decorators = [api_login_required]

	def getModel(self):
		return Commit

class CommitsDetailController(APIDetailView):
	methods = ['GET', 'PUT', 'DELETE']
	decorators = [api_login_required]

	def getModel(self):
		return Commit
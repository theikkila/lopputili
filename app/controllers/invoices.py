from .listview import APIListView, APIDetailView
from .login import api_login_required
from ..models.invoice import Invoice

class InvoicesListController(APIListView):
	methods = ['GET', 'POST']
	decorators = [api_login_required]

	def getModel(self):
		return Invoice

class InvoicesDetailController(APIDetailView):
	methods = ['GET', 'PUT', 'DELETE']
	decorators = [api_login_required]

	def getModel(self):
		return Invoice
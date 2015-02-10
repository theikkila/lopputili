from .listview import APIListView, APIDetailView
from .login import login_required
from ..models.invoice import Invoice

class InvoicesListController(APIListView):
	methods = ['GET', 'POST']
	decorators = [login_required]

	def getModel(self):
		return Invoice

class InvoicesDetailController(APIDetailView):
	methods = ['GET', 'PUT', 'DELETE']
	decorators = [login_required]

	def getModel(self):
		return Invoice
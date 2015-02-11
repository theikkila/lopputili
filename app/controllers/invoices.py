from .listview import APIListView, APIDetailView
from .login import api_login_required
from ..models.invoice import Invoice

class InvoicesListController(APIListView):

	def getModel(self):
		return Invoice

class InvoicesDetailController(APIDetailView):

	def getModel(self):
		return Invoice
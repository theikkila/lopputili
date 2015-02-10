from .listview import APIListView, APIDetailView
from .login import login_required
from ..models.contact import Contact

class ContactsListController(APIListView):
	methods = ['GET', 'POST']
	decorators = [login_required]

	def getModel(self):
		return Contact

class ContactsDetailController(APIDetailView):
	methods = ['GET', 'PUT', 'DELETE']
	decorators = [login_required]

	def getModel(self):
		return Contact
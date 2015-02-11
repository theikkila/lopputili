from .listview import APIListView, APIDetailView
from .login import api_login_required
from ..models.contact import Contact

class ContactsListController(APIListView):

	def getModel(self):
		return Contact

class ContactsDetailController(APIDetailView):

	def getModel(self):
		return Contact
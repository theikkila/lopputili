from .listview import APIListView, APIDetailView
from .login import login_required
from ..models.account import Account

class AccountsListController(APIListView):
	methods = ['GET', 'POST']
	decorators = [login_required]

	def getModel(self):
		return Account

class AccountsDetailController(APIDetailView):
	methods = ['GET', 'PUT', 'DELETE']
	decorators = [login_required]

	def getModel(self):
		return Account
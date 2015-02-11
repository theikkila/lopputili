from .listview import APIListView, APIDetailView
from .login import api_login_required
from ..models.account import Account

class AccountsListController(APIListView):
	methods = ['GET', 'POST']
	decorators = [api_login_required]

	def getModel(self):
		return Account

class AccountsDetailController(APIDetailView):
	methods = ['GET', 'PUT', 'DELETE']
	decorators = [api_login_required]

	def getModel(self):
		return Account
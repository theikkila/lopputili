from .listview import APIListView, APIDetailView
from .login import api_login_required
from ..models.account import Account

class AccountsListController(APIListView):

	def getModel(self):
		return Account

class AccountsDetailController(APIDetailView):

	def getModel(self):
		return Account
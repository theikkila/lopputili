import os


from . import query
from . import sql
Database = sql.Database
Query = query.Query



class ORM:
	def __init__(self):
		self.models = []
		self.dburi = os.getenv('DATABASE_URL', "sqlite://local.db")
		self.db = Database(self.dburi)

	def registerModel(self, model):
		model.setDB(self.db)
		self.models.append(model)

	def initTables(self):
		for model in self.models:
			try:
				self.db.createTables(model)
			except:
				return False
		return True
import os


from . import query
from . import sql
from sqlite3 import OperationalError
from psycopg2 import ProgrammingError
Database = sql.Database
Query = query.Query



class ORM:
	def __init__(self):
		self.models = []
		self.nmodels = {}
		self.dburi = os.getenv('DATABASE_URL', "sqlite://local.db")
		self.db = Database(self.dburi)

	def registerModel(self, model):
		model.setDB(self.db, self)
		self.models.append(model)
		self.nmodels[model.__name__] = model
		#print(self.nmodels)

	def initTables(self):
		for model in self.models:
			try:
				self.db.createTables(model)
			except OperationalError:
				return False
			except ProgrammingError:
				return False
		return True
import os
import urlparse
import sqlite3
import psycopg2

urlparse.uses_netloc.append("postgres")
urlparse.uses_netloc.append("sqlite")

class ORM:
	def __init__(self):
		self.models = []
		self.dburi = urlparse.urlparse(os.getenv('DATABASE_URL', "sqlite://local.db"))
		self.db = self.dburi.scheme
		if self.db == "postgres":
			self.conn = psycopg2.connect(
							database=url.path[1:],
							user=url.username,
							password=url.password,
							host=url.hostname,
							port=url.port
						)
			self.c = self.conn.cursor()
		else:
			self.db = "sqlite"
			self.conn = sqlite3.connect(self.dburi.netloc)
			def dict_factory(cursor, row):
				d = {}
				for idx, col in enumerate(cursor.description):
					d[col[0]] = row[idx]
				return d
			self.conn.row_factory = dict_factory
			self.c = self.conn.cursor()

	def registerModel(self, model):
		model.setDB(self.db, self.conn)
		self.models.append(model)

	def initTables(self):
		for model in self.models:
			try:
				model.createTables()
			except sqlite3.OperationalError:
				return False
		return True
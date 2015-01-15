import os
import urlparse
import querybuilder


urlparse.uses_netloc.append("postgres")
urlparse.uses_netloc.append("sqlite")

class ORM:
	def __init__(self):
		self.models = []
		self.dburi = urlparse.urlparse(os.getenv('DATABASE_URL', "sqlite://local.db"))
		self.db = self.dburi.scheme

		if self.db == "postgres":
			import psycopg2
			self.conn = psycopg2.connect(
						    database=url.path[1:],
							user=url.username,
							password=url.password,
							host=url.hostname,
							port=url.port
						)
			self.c = self.conn.cursor()
		else:
			import sqlite3
			self.conn = sqlite3.connect(self.dburi.netloc)
			self.c = self.conn.cursor()

	def registerModel(self, model):
		self.models.append(model)

	def initTables(self):
		try:
			for model in self.models:
				self.c.execute(querybuilder.createTable(self.db, model))
		except:
			return False
		return True
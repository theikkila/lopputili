import os
import urllib.parse
import sqlite3
import psycopg2
import psycopg2.extras

from . import query
Query = query.Query

urllib.parse.uses_netloc.append("postgres")
urllib.parse.uses_netloc.append("sqlite")

class ORM:
	def __init__(self):
		self.models = []
		self.dburi = urllib.parse.urlparse(os.getenv('DATABASE_URL', "sqlite://local.db"))
		self.db = self.dburi.scheme
		if self.db == "postgres":
			self.conn = psycopg2.connect(
							database=self.dburi.path[1:],
							user=self.dburi.username,
							password=self.dburi.password,
							host=self.dburi.hostname,
							port=self.dburi.port,
							cursor_factory=psycopg2.extras.RealDictCursor
						)
			self.conn.autocommit = True
			self.c = self.conn.cursor()
		else:
			self.db = "sqlite"
			self.conn = sqlite3.connect(self.dburi.netloc, check_same_thread=False)
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
			except:
				return False
		return True
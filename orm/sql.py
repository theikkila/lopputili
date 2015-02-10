from . import dbwords
from . import exceptions

import urllib.parse
import sqlite3
import psycopg2
import psycopg2.extras

urllib.parse.uses_netloc.append("postgres")
urllib.parse.uses_netloc.append("sqlite")


def return_iterator(so1, so2):
	if so1 is None:
		return so2
	return so1

class Database:
	def __init__(self, dburi):
		parsed_dburl = urllib.parse.urlparse(dburi)
		self.db = parsed_dburl.scheme
		if self.db == "postgres":
			self.conn = psycopg2.connect(
							database=parsed_dburl.path[1:],
							user=parsed_dburl.username,
							password=parsed_dburl.password,
							host=parsed_dburl.hostname,
							port=parsed_dburl.port,
							cursor_factory=psycopg2.extras.RealDictCursor
						)
			self.conn.autocommit = True
		else:
			self.db = "sqlite"
			self.conn = sqlite3.connect(parsed_dburl.netloc, check_same_thread=False)
			def dict_factory(cursor, row):
				d = {}
				for idx, col in enumerate(cursor.description):
					d[col[0]] = row[idx]
				return d
			self.conn.row_factory = dict_factory
			self.conn.cursor().execute("PRAGMA foreign_keys = ON")
		self.cursor = self.conn.cursor()

	def createTableSQL(self, model):
		field_names = model.getfields()
		fields = []
		contrs = []
		for field_name in field_names:
			f = getattr(model, '_'+field_name)
			ft = model.fieldtype(field_name)
			typevars = dict(list(getattr(model, '_'+field_name).meta.items())+list({"key": field_name}.items()))
			sqtype = dbwords.gettype(self.db, ft) % typevars
			splitted = sqtype.split(',')
			sqtype = splitted[0]
			if len(splitted) > 1:
				contrs.append(splitted[1])
			#print(sqtype)
			field = field_name + " " + sqtype
			fields.append(field)
		#print ", ".join(fields)
		return 'CREATE TABLE {table} ({fields})'.format(table=model.tableName(), fields=", ".join(fields+contrs))

	def createTables(self, model):
		cursor = self.conn.cursor()
		sql = self.createTableSQL(model)
		#print(sql)
		cursor.execute(sql)

	def parse_query(self, query):
		if self.db == 'postgres':
			return query.replace('?', '%s')
		return query

	def query(self, raw_query, raw_params=None, commit=False):
		self.cursor = self.conn.cursor()
		q = self.parse_query(raw_query)

		print(q)
		params = self.parse_params(raw_params)
		if params:
			res = self.cursor.execute(q, params)
		else:
			res = self.cursor.execute(q)	
		if commit:
			self.conn.commit()
		iterator = return_iterator(res, self.cursor)
		return iterator

	def parse_params(self, params):
		if not params:
			return None
		if type(params) not in [tuple, list, object]:
			return (params,)
		return params

	def insert(self, table, serialized):
		del serialized['pk']
		keys = ', '.join(list(serialized.keys()))
		
		qmarks = ', '.join('?' * len(serialized))
		raw_query = "INSERT INTO %s (%s) VALUES (%s)" % (table, keys, qmarks)
		res = self.query(raw_query, list(serialized.values()), True)

		if self.cursor.lastrowid != None:
			return self.cursor.lastrowid
		return res

	def update(self, table, serialized):
		pk = serialized['pk']
		del serialized['pk']
		updatepairs = ', '.join([key+" = ?" for key in list(serialized.keys())])
		raw_query = "UPDATE %s SET %s WHERE pk = ?" % (table, updatepairs)
		res = self.query(raw_query, list(serialized.values())+[pk])
		return res

	def delete(self, table, pk):
		raw_query = "DELETE FROM %s WHERE pk = ?" % table
		res = self.query(raw_query, pk, True)
		return res

	def getById(self, table, pk):
		raw_query = "SELECT * FROM %s WHERE pk = ?" % table
		res = self.query(raw_query, pk)
		return res.fetchone()

	def filter(self, table, query):
		base_query = "SELECT * FROM %s WHERE " % table

		values = []
		sql_parts = []
		for sqlpart, value in query.sqls(dbwords.curryOperator(self.db)):
			values.append(value)
			sql_parts.append(sqlpart)
		raw_query = base_query + " AND ".join(sql_parts)
		return self.query(raw_query, values)

	def all(self, table):
		return self.query("SELECT * FROM %s" % table)

	def exportData(self):
		tables_sql_pg = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
		tables_sql_lite = 'SELECT name FROM sqlite_master WHERE type = "table";'
		self.cursor = self.conn.cursor()
		if self.db == 'postgres':
			tables_query = tables_sql_pg
		else:
			tables_query = tables_sql_lite
		res = self.cursor.execute(tables_query)
		all_tables = []
		for table in res.fetchall():
			t = {"name":table['name'], "headers":[], "rows":[]}
			rows = self.cursor.execute('SELECT * FROM %s' % table['name'])
			for row in rows.fetchall():
				if len(t['headers']) == 0:
					t['headers'] = list(row.keys())
				trow = []
				for header in t['headers']:
					#print(header)
					#print(row)
					trow.append(row.get(header, '---'))
				t["rows"].append(trow)
			all_tables.append(t)
		return all_tables
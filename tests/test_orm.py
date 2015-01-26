import unittest
import os

from orm import ORM

from orm import models
from orm import fields

class User(models.Model):
	first_name = fields.CharField(max_length=40, blank=True)
	last_name = fields.CharField(max_length=40, blank=True)
	username = fields.CharField(max_length=40)
	password = fields.CharField(max_length=40)


testDBpath = "test.db"

class ormTest(unittest.TestCase):
	def setUp(self):
		if os.path.isfile(testDBpath):
			os.remove(testDBpath)
		self.o = ORM()

	def tearDown(self):
		if os.path.isfile(testDBpath):
			os.remove(testDBpath)

	def testCreateDB(self):
		self.assertTrue(os.path.isfile(testDBpath))

	def testOrmInit(self):
		self.assertEqual(self.o.db.db, "sqlite")

	def testRegisterModel(self):
		self.o.registerModel(User)
		self.assertEqual(len(self.o.models), 1)
		self.assertTrue(self.o.initTables())
		r = self.o.db.query("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
		self.assertEqual(r.fetchone(), {"name": "users"})
		self.o.db.query("SELECT * FROM users")
		self.assertEqual(set([x[0] for x in self.o.db.cursor.description]), set(['first_name', 'last_name', 'password', 'pk', 'username']))

if __name__ == '__main__':
    unittest.main()
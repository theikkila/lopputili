import unittest
import os

from orm import ORM
from orm import model
from orm import fields
from orm import exceptions

class User2(model.Model):
	first_name = fields.CharField(max_length=40, blank=True)

class User(model.Model):
	first_name = fields.CharField(max_length=40, blank=True)
	last_name = fields.CharField(max_length=40, blank=True)
	username = fields.CharField(max_length=40)
	password = fields.CharField(max_length=40)

testDBpath = "test.db"

class modelTest(unittest.TestCase):

	def setUp(self):
		if os.path.isfile(testDBpath):
			os.remove(testDBpath)
		self.o = ORM()
		self.o.registerModel(User)

	def tearDown(self):
		if os.path.isfile(testDBpath):
			os.remove(testDBpath)

	def test_tablename(self):
		self.assertEqual(User.tableName(), 'users')

	def test_getfields(self):
		self.assertEqual(set(User.getfields()), set([ 'first_name', 'last_name', 'password', 'pk', 'username']))

	#def test_modelSQL(self):
	#	self.assertEqual(User.createTableSQL(), "CREATE TABLE users (password varchar(40), first_name varchar(40), last_name varchar(40), pk integer primary key, username varchar(40))")

	def test_notregistered(self):
		self.assertRaises(exceptions.ModelNotRegisteredError, User2.createTableSQL)

if __name__ == '__main__':
    unittest.main()
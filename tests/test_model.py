import unittest
import os

from orm import ORM
from orm import model
from orm import fields
from orm import exceptions
from orm import Query

class User2(model.Model):
	first_name = fields.CharField(max_length=40, blank=True)

class User(model.Model):
	first_name = fields.CharField(max_length=40, blank=True)
	last_name = fields.CharField(max_length=40, blank=True)
	username = fields.CharField(max_length=40)
	password = fields.CharField(max_length=40)

	def __str__(self):
		return self.first_name+" "+self.last_name

testDBpath = "test.db"

class modelTest(unittest.TestCase):

	def setUp(self):
		if os.path.isfile(testDBpath):
			os.remove(testDBpath)
		self.o = ORM()
		self.o.registerModel(User)
		self.o.initTables()

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
		self.assertRaises(exceptions.ModelNotRegisteredError, User2.all)

	def test_basic_save(self):
		u = User(first_name="Testi", last_name="Last von Name", username="testuser", password="testpasswd")
		self.assertEqual(u.pk, None)
		self.assertEqual(u.first_name, "Testi")
		self.assertEqual(u.last_name, "Last von Name")
		u.save()
		self.assertEqual(u.pk, 1)

	def test_basic_get(self):
		a = User(username="testuser", password="testpasswd").save()
		u = User.get(a.pk)
		self.assertEqual(u.username, a.username)
		self.assertEqual(u.password, a.password)
		self.assertEqual(u.pk, a.pk)

	def test_basic_all(self):
		for x in range(10):
			User(username="user"+str(x), password="testpasswd").save()
		collection = User.all()
		self.assertEqual(len(collection), 10)

	def test_basic_collection_filter(self):
		for x in range(10):
			User(username="user"+str(x), password="testpasswd").save()
		collection = User.all()
		self.assertEqual(len(collection), 10)
		self.assertEqual(len(collection.filter(pk__gt=5)), 5)

if __name__ == '__main__':
    unittest.main()
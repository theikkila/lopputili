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
	pets = fields.HasField('Pet', 'owner')

	def __str__(self):
		return self.first_name+" "+self.last_name

class Pet(model.Model):
	name = fields.CharField(max_length=40, blank=True)
	owner = fields.ForeignKeyField(User)

testDBpath = "test.db"

class modelTest(unittest.TestCase):

	def setUp(self):
		if os.path.isfile(testDBpath):
			os.remove(testDBpath)
		self.o = ORM(os.getenv('DATABASE_URL', "sqlite://local.db"))
		if self.o.db.db == "postgres":
			self.o.db.cursor.execute("drop schema public cascade")
			self.o.db.cursor.execute("create schema public")
		self.o.registerModel(User)
		self.o.registerModel(Pet)
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

	def test_foreignkey(self):
		a = User(first_name="Paul", last_name="Petowner", username="testuser", password="testpasswd").save()
		p = Pet(name="Fluffy", owner=a).save()
		np = Pet.get(p.pk)
		self.assertEqual(np.owner.username, 'testuser')
		np.owner.username = "testuser2"
		np.owner.save()
		self.assertEqual(np.owner.username, 'testuser2')

	def test_reverse_relation(self):
		a = User(first_name="Paul", last_name="Petowner", username="testuser", password="testpasswd").save()
		b = Pet(name="Fluffy", owner=a).save()
		c = Pet(name="Bluffy", owner=a).save()
		collection = a.pets
		self.assertEqual(len(collection), 2)
		self.assertEqual(collection[0].name, b.name)

	def test_delete_cascade(self):
		a = User(first_name="Paul", last_name="Petowner", username="testuser", password="testpasswd").save()
		b = Pet(name="Fluffy", owner=a).save()
		c = Pet(name="Bluffy", owner=a).save()
		collection = a.pets
		self.assertEqual(len(collection), 2)
		self.assertEqual(collection[0].name, b.name)
		a.delete()
		self.assertEqual(len(a.pets), 0)

if __name__ == '__main__':
    unittest.main()
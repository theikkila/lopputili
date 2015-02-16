import unittest
import os
import subprocess
import requests
import threading
from time import sleep
import json

class Runner(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None

    def run(self):
        print("Starting " + self.name)
        e = os.environ.copy()
        e['DATABASE_URL'] = "sqlite://test.db"
        cmd = ['python', 'lopputili.py']
        self.process = p = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     env=e)
        for line in iter(p.stdout.readline, b''):
            print("-------> " + str(line.rstrip()))
        print("Exiting " + self.name)

    def stop(self):
        print("Trying to stop thread ")
        if self.process is not None:
            self.process.terminate()
            self.process = None


testDBpath = "test.db"
headers = {"content-type":"application/json"}

server_path = "http://localhost:3000"

class apiTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.sr = Runner()
		cls.sr.start()
		sleep(4)
		r = requests.post(server_path+'/login', data={"username":"test", "password":"test"})
		cls.auth_cookies = r.cookies

	@classmethod
	def tearDownClass(cls):
		cls.sr.stop()

	def test_is_server_up(self):
		r = requests.get(server_path+'/login')
		self.assertEqual(r.status_code, 200)

	def test_if_cannot_access_without_credientials(self):
		r = requests.get(server_path+'/api/receipts')
		self.assertEqual(r.status_code, 403)
		
	def test_object_not_found(self):
		r = requests.get(server_path+'/api/receipts/96', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 404)
		

	def test_receipts_crud(self):
		model = 'receipts'
		r = requests.get(server_path+'/api/'+model+'', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), {"data":[]})
		obj = {
			"rid":1001,
			"owner": 1,
			"commit_date": "2015-02-11T11:46:30.670Z",
			"description": "Kuvaus kirjanpitotapahtumasta"
			}
		r = requests.post(server_path+'/api/'+model+'', data=json.dumps(obj), headers=headers, cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 201)
		r = requests.get(server_path+'/api/'+model+'', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		shouldbe = {'data': [{
			'commit_date': '2015-02-11T11:46:30.670000Z',
            'description': 'Kuvaus kirjanpitotapahtumasta',
            'owner': 1,
            'pk': 1,
            'rid': 1001
            }]}
		self.assertEqual(r.json(), shouldbe)
		r = requests.get(server_path+'/api/'+model+'/1', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), shouldbe['data'][0])
		shouldbe['data'][0]['description'] = "Uusi kuvaus"
		r = requests.put(server_path+'/api/'+model+'/1', cookies=self.auth_cookies, data=json.dumps(shouldbe['data'][0]), headers=headers)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), shouldbe['data'][0])
		r = requests.get(server_path+'/api/'+model+'/1', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), shouldbe['data'][0])
		r = requests.delete(server_path+'/api/'+model+'/1', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		r = requests.get(server_path+'/api/'+model+'', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), {"data":[]})

	def test_wrong_data(self):
		obj = {
			"address":"Vain osoite"
			}
		r = requests.post(server_path+'/api/contacts', data=json.dumps(obj), headers=headers, cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 400)

	def test_contacts_crud(self):
		model = 'contacts'
		r = requests.get(server_path+'/api/'+model+'', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), {"data":[]})
		obj = {
			"name":"Testi Yhteystieto"
			}
		r = requests.post(server_path+'/api/'+model+'', data=json.dumps(obj), headers=headers, cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 201)
		r = requests.get(server_path+'/api/'+model+'', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		shouldbe = {'data': [{
			'pk': 1,
			'owner': 1,
			'name': "Testi Yhteystieto",
			'address': None,
			'zip_code': None,
			'city': None,
			'email': None
            }]}
		self.assertEqual(r.json(), shouldbe)
		r = requests.get(server_path+'/api/'+model+'/1', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), shouldbe['data'][0])
		shouldbe['data'][0]['address'] = "Osoite 12"
		r = requests.put(server_path+'/api/'+model+'/1', cookies=self.auth_cookies, data=json.dumps(shouldbe['data'][0]), headers=headers)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), shouldbe['data'][0])
		r = requests.get(server_path+'/api/'+model+'/1', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), shouldbe['data'][0])
		r = requests.delete(server_path+'/api/'+model+'/1', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		r = requests.get(server_path+'/api/'+model+'', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), {"data":[]})



	def test_is_accounts_empty(self):
		r = requests.get(server_path+'/api/accounts', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), {"data":[]})

	def test_is_commits_empty(self):
		r = requests.get(server_path+'/api/commits', cookies=self.auth_cookies)
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.json(), {"data":[]})

if __name__ == '__main__':
	unittest.main()
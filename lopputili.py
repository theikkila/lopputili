# encoding: utf-8
from flask import Flask
from orm import ORM
from app.models.account import Account
from app.models.user import User

import markdown2

app = Flask(__name__)


@app.route('/app')
def hello_app():
	o = ORM()
	o.registerModel(Account)
	o.registerModel(User)
	if o.initTables():
		return "Taulut luotu!"
	else:
		return "Taulujen luonti epäonnistui!"

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/esittelysivu')
def introduction():
    return markdown2.markdown_path('doc/generated/documentation.md')

if __name__ == '__main__':
    app.run(debug=True)
# encoding: utf-8
import os
from flask import Flask, request, render_template
from orm import ORM
from app.models.account import Account
from app.models.user import User
from app.controllers.receipts import ReceiptsController
from app.controllers.login import LoginController, logout

from app.models.statistics import Visit

import markdown2, datetime

app = Flask(__name__)

o = ORM()
o.registerModel(Account)
o.registerModel(User)
o.registerModel(Visit)
o.initTables()

u = User(username="test", password="test").save()

@app.route('/')
def hello_world():
	s = Visit(useragent=request.headers.get('User-Agent'), time=datetime.datetime.now())
	s.save()
	
	a = Visit.all()
	return render_template('hello.html', uas=sorted(a, key=lambda visit: visit.time)[len(a)-10:], count=len(a))

@app.route('/connectiontest')
def connectiontest():
	data = o.db.exportData()
	return render_template('connectiontest.html', data=data)


@app.route('/esittelysivu')
def introduction():
    return markdown2.markdown_path('doc/generated/documentation.md')


# Real routes

@app.route('/settings')
def settings():
	return render_template('settings.html')

@app.route('/contacts')
def contacts():
	return render_template('contacts.html')

@app.route('/invoices')
def invoices():
	return render_template('invoices.html')



app.add_url_rule('/login', view_func=LoginController.as_view('login'))
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/receipts', view_func=ReceiptsController.as_view('receipts'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 3000)))
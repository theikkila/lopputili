# encoding: utf-8
import os
from flask import Flask, request, render_template
from orm import ORM
from app.models.account import Account
from app.models.user import User
from app.models.contact import Contact
from app.models.receipt import Receipt, Commit
from app.controllers.receipts import ReceiptsListController, ReceiptsDetailController, CommitsListController, CommitsDetailController
from app.controllers.accounts import AccountsListController, AccountsDetailController
from app.controllers.contacts import ContactsListController, ContactsDetailController
from app.controllers.login import LoginController, logout, login_required

from app.models.statistics import Visit

import markdown2, datetime

app = Flask(__name__)

o = ORM()
o.registerModel(Account)
o.registerModel(User)
o.registerModel(Visit)
o.registerModel(Receipt)
o.registerModel(Commit)
o.registerModel(Contact)
o.initTables()

def FullRESTendpoint(app, name, listcontroller, detailcontroller):
	app.add_url_rule('/api/'+name, view_func=listcontroller.as_view(name))
	app.add_url_rule('/api/'+name+'/<pk>', view_func=detailcontroller.as_view(name+'_detail'))
	app.add_url_rule('/api/'+name+'/<pk>/<field>', view_func=detailcontroller.as_view(name+'_detail_field'))


u = User(username="test", password="test").save()

@app.route('/visit')
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

def dashboard():
	return render_template('base.html')

@app.route('/invoices')
def invoices():
	return render_template('invoices.html')



app.add_url_rule('/login', view_func=LoginController.as_view('login'))
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/', 'dashboard', login_required(dashboard))


FullRESTendpoint(app, 'receipts', ReceiptsListController, ReceiptsDetailController)
FullRESTendpoint(app, 'commits', CommitsListController, CommitsDetailController)
FullRESTendpoint(app, 'accounts', AccountsListController, AccountsDetailController)
FullRESTendpoint(app, 'contacts', ContactsListController, ContactsDetailController)

app.secret_key = os.getenv('SECRET_KEY', 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 3000)))
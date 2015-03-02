# encoding: utf-8
import os
from flask import Flask, request, render_template, session
from orm import ORM
from app.models.account import Account
from app.models.user import User
from app.models.contact import Contact
from app.models.receipt import Receipt, Commit
from app.models.invoice import Invoice, Product
from app.models.setting import Setting
from app.controllers.receipts import ReceiptsListController, ReceiptsDetailController, CommitsListController, CommitsDetailController
from app.controllers.accounts import AccountsListController, AccountsDetailController
from app.controllers.contacts import ContactsListController, ContactsDetailController
from app.controllers.invoices import InvoicesListController, InvoicesDetailController, ProductsListController, ProductsDetailController, InvoiceGeneratorController
from app.controllers.settings import SettingsController
from app.controllers.login import LoginController, logout, login_required


import markdown2, datetime

app = Flask(__name__)

o = ORM(os.getenv('DATABASE_URL', "sqlite://local.db"))
o.registerModel(Account)
o.registerModel(User)
o.registerModel(Receipt)
o.registerModel(Commit)
o.registerModel(Contact)
o.registerModel(Invoice)
o.registerModel(Product)
o.registerModel(Setting)
o.initTables()

def FullRESTendpoint(app, name, listcontroller, detailcontroller):
	app.add_url_rule('/api/'+name, view_func=listcontroller.as_view(name))
	app.add_url_rule('/api/'+name+'/<pk>', view_func=detailcontroller.as_view(name+'_detail'))
	app.add_url_rule('/api/'+name+'/<pk>/<field>', view_func=detailcontroller.as_view(name+'_detail_field'))

try:
	User.get(1)
except:
	u = User(username="test").set_password('test').save()

@app.route('/connectiontest')
def connectiontest():
	data = o.db.exportData()
	return render_template('connectiontest.html', data=data)


@app.route('/esittelysivu')
def introduction():
    return markdown2.markdown_path('doc/generated/documentation.md', extras=["tables"])


# Real routes

def dashboard():
	return render_template('base.html', owner_pk=session['logged_in'])


app.add_url_rule('/login', view_func=LoginController.as_view('login'))
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/', 'dashboard', login_required(dashboard))
app.add_url_rule('/api/settings', view_func=SettingsController.as_view('settings'))
app.add_url_rule('/api/invoices/<pk>/generate', view_func=InvoiceGeneratorController.as_view('invoice_generator'))

FullRESTendpoint(app, 'receipts', ReceiptsListController, ReceiptsDetailController)
FullRESTendpoint(app, 'commits', CommitsListController, CommitsDetailController)
FullRESTendpoint(app, 'accounts', AccountsListController, AccountsDetailController)
FullRESTendpoint(app, 'contacts', ContactsListController, ContactsDetailController)
FullRESTendpoint(app, 'invoices', InvoicesListController, InvoicesDetailController)
FullRESTendpoint(app, 'products', ProductsListController, ProductsDetailController)

app.secret_key = os.getenv('SECRET_KEY', 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 3000)))
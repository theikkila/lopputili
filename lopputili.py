# encoding: utf-8
from flask import Flask, request, render_template

from orm import ORM
from app.models.account import Account
from app.models.user import User

from app.models.statistics import Visit

import markdown2, datetime

app = Flask(__name__)

o = ORM()
o.registerModel(Account)
o.registerModel(User)
o.registerModel(Visit)
o.initTables()

@app.route('/')
def hello_world():
	s = Visit(useragent=request.headers.get('User-Agent'), time=datetime.datetime.now())
	s.save()
	a = Visit.all()
	return render_template('hello.html', uas=a[len(a)-10:], count=len(a))

@app.route('/esittelysivu')
def introduction():
    return markdown2.markdown_path('doc/generated/documentation.md')

if __name__ == '__main__':
    app.run(debug=True)
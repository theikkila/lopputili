from flask.views import View
from flask import render_template, session, redirect, url_for, request, flash
from app.models.user import User

def login_required(f):
	"""Checks whether user is logged in or redirects login page"""
	def decorator(*args, **kwargs):
		print(session)
		if not "logged_in" in session:
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorator

class LoginController(View):
	methods = ['GET', 'POST']

	def dispatch_request(self):
		if request.method == 'GET':
			return render_template('login.html')
		try:
			a = User.filter(username__exact=request.form['username'])
			if len(a) < 1 or a[0] is None:
				raise Exception("Invalid username or password")
			user = a[0]
			if user.is_valid_password(request.form['password']):
				session['logged_in'] = user.pk
				return redirect(url_for('receipts'))
			else:
				raise Exception("Invalid username or password")
		except Exception as e:
			return render_template('login.html', e=e)

def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))
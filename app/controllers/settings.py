from flask.views import MethodView
from flask import render_template, session, redirect, url_for, request, flash, jsonify
from app.models.user import User
from .login import api_login_required

class SettingsController(MethodView):
	methods = ['GET']
	decorators = [api_login_required]

	def get(self):
		return jsonify({})
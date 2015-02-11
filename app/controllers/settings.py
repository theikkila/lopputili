from flask.views import MethodView
from flask import render_template, session, redirect, url_for, request, flash, jsonify
from app.models.user import User
from app.models.setting import Setting
from .login import api_login_required

class SettingsController(MethodView):
	methods = ['GET', 'PUT']
	decorators = [api_login_required]

	def get(self):
		try:
			setting = Setting.filter(owner__exact=session['logged_in'])[0]
		except:
			setting = Setting(owner=session['logged_in']).save()
		return jsonify(setting.serialize())

	def put(self):
		try:
			setting = Setting.filter(owner__exact=session['logged_in'])[0]
		except:
			setting = Setting(owner=session['logged_in']).save()
		new_setting = Setting.deserialize(request.json)
		new_setting.pk = setting.pk
		new_setting.owner = setting.owner.pk
		new_setting.save()
		return jsonify(new_setting.serialize())

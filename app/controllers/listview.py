from flask.views import MethodView
from flask import request, session
from flask import jsonify
from orm.fields import HasField
from orm.exceptions import FieldNotValidError, ObjectNotFoundError
from .login import api_login_required

'''
 These two classes implements basic JSON REST-api
'''

class APIListView(MethodView):
	methods = ['GET', 'POST']
	decorators = [api_login_required]

	def getModel(self):
		raise Exception("Model not defined")

	def get(self):
		objects = self.getModel().filter(owner__exact=session['logged_in']).serialize()
		resp = jsonify({"data":objects})
		resp.status_code = 200
		return resp

	def post(self):
		Model = self.getModel()
		try:
			populated_model = Model.deserialize(request.json, True)
			populated_model.owner = session['logged_in']
			populated_model.save()
			resp = jsonify(populated_model.serialize())
			resp.status_code = 201 # created
			return resp
		except FieldNotValidError as e:
			resp = jsonify({"error": "Field '" + str(e) + "' is not valid!", "code": 400})
			resp.status_code = 400
			return resp
			
		except Exception as e:
			resp = jsonify({"error": str(e), "code": 400})
			resp.status_code = 400
			return resp

class APIDetailView(MethodView):
	methods = ['GET', 'PUT', 'DELETE']
	decorators = [api_login_required]

	def getModel(self):
		raise Exception("Model not defined")

	def get(self, pk, field=None):
		try:
			obj = self.getModel().get(pk)
			if obj.owner.pk != session['logged_in']:
				raise ObjectNotFoundError("Access denied")
		except ObjectNotFoundError as e:
			resp = jsonify({"error": "Object not found", "code": 404})
			resp.status_code = 404
			return resp

		if field and hasattr(obj, field) and hasattr(obj, '_'+field) and  isinstance(getattr(obj, '_'+field), HasField):
			ret = {}
			ret['data'] = getattr(obj, field).serialize()
			resp = jsonify(ret)
			resp.status_code = 200
			return resp
		resp = jsonify(obj.serialize())
		resp.status_code = 200
		return resp

	def put(self, pk, field=None):
		try:
			obj = self.getModel().get(pk)
			if obj.owner.pk != session['logged_in']:
				raise ObjectNotFoundError("Access denied")
			populated_model = self.getModel().deserialize(request.json)
			populated_model.owner = session['logged_in']
			populated_model.save()
			resp = jsonify(populated_model.serialize())
			resp.status_code = 200
			return resp

		except FieldNotValidError as e:
			resp = jsonify({"error": "Field '" + str(e) + "' is not valid!", "code": 400})
			resp.status_code = 400
			return resp
			
		except Exception as e:
			resp = jsonify({"error": str(e), "code": 400})
			resp.status_code = 400
			return resp

	def delete(self, pk, field=None):
		try:
			obj = self.getModel().get(pk)
			if obj.owner.pk != session['logged_in']:
				raise ObjectNotFoundError("Access denied")
			resp = jsonify(obj.serialize())
			obj.delete()
			resp.status_code = 200
			return resp
		except Exception as e:
			resp = jsonify({"error": str(e), "code": 400})
			resp.status_code = 400
			return resp
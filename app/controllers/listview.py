from flask.views import MethodView
from flask import request
from flask import jsonify
from orm.fields import HasField

class APIListView(MethodView):

	def getModel(self):
		raise Exception("Model not defined")

	def get(self):
		objects = self.getModel().all().serialize()
		resp = jsonify({"data":objects})
		resp.status_code = 200
		return resp

	def post(self):
		Model = self.getModel()
		populated_model = Model.deserialize(request.json, True)
		populated_model.save()
		resp = jsonify(populated_model.serialize())
		resp.status_code = 201 # created
		return resp

class APIDetailView(MethodView):

	def getModel(self):
		raise Exception("Model not defined")

	def get(self, pk, field=None):
		obj = self.getModel().get(pk)
		if field and hasattr(obj, field) and hasattr(obj, '_'+field) and  isinstance(getattr(obj, '_'+field), HasField):
			ret = {}
			ret[field] = getattr(obj, field).serialize()
			resp = jsonify(ret)
			resp.status_code = 200
			return resp
		resp = jsonify(obj.serialize())
		resp.status_code = 200
		return resp

	def put(self, pk, field=None):
		populated_model = Model.deserialize(request.json)
		populated_model.save()
		resp.jsonify(populated_model.serialize())
		resp.status_code = 200

	def delete(self, pk, field=None):
		obj = self.getModel().get(pk)
		resp = jsonify(obj.serialize())
		obj.delete()
		resp.status_code = 200
		return resp
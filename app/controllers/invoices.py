from .listview import APIListView, APIDetailView
from flask.views import MethodView
from flask import request, session
from flask import jsonify, send_file
from orm.exceptions import FieldNotValidError, ObjectNotFoundError
from .login import api_login_required
from ..models.invoice import Invoice, Product
from app.models.setting import Setting
from lib import finv2pdf
from io import BytesIO

class InvoicesListController(APIListView):

	def getModel(self):
		return Invoice

class InvoicesDetailController(APIDetailView):

	def getModel(self):
		return Invoice

class InvoiceGeneratorController(MethodView):
	methods = ['GET']
	decorators = [api_login_required]

	def get(self, pk, field=None):
		try:
			invoice = Invoice.get(pk)
			if invoice.owner.pk != session['logged_in']:
				raise ObjectNotFoundError("Access denied")
		except ObjectNotFoundError as e:
			resp = jsonify({"error": "Object not found", "code": 404})
			resp.status_code = 404
			return resp
		dformat = "%d.%m.%Y"
		setting = Setting.filter(owner__exact=session['logged_in'])[0]
		summ = 0
		for product in invoice.products:
			l = product.price * product.count
			n = (l - l * (product.discount/100))
			summ += n + n * (product.vat/100)
		company = finv2pdf.Company(setting.company_name, setting.address, setting.zip_code, setting.city, setting.phone, setting.email, setting.city, setting.vat_code, setting.iban, setting.bic)
		invdata = finv2pdf.InvoiceData(invoice.created.strftime(dformat), str(invoice.invoice_id), str(invoice.ref), str(invoice.contact.pk), '%s'%invoice.our_ref, '%s'%invoice.your_ref, invoice.payment_type, invoice.due_date.strftime(dformat), str(invoice.reclamation_time), str(invoice.penalty_interest), summ, invoice.info1, invoice.info2)
		client = finv2pdf.Client(invoice.contact.name, invoice.contact.address, invoice.contact.zip_code, invoice.contact.city)
		response = BytesIO()
		inv = finv2pdf.Invoice2PDF("invoice", response)
		inv.createInvoice(invdata, company, client)
		for product in invoice.products:
			inv.drawProduct(product.name, product.count, product.price, product.vat, product.discount)
		inv.ready()
		inv.save()
		response.seek(0)
		return send_file(response,
                     attachment_filename="invoice.pdf",
                     as_attachment=True)


class ProductsListController(APIListView):

	def getModel(self):
		return Product

class ProductsDetailController(APIDetailView):

	def getModel(self):
		return Product
from flask.views import View
from flask import render_template

class ReceiptsController(View):
    methods = ['GET']

    def dispatch_request(self, name):
        return render_template('receipts.html', name=name)
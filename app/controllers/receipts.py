from flask.views import View
from flask import render_template
from .login import login_required

class ReceiptsController(View):
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self):
        return render_template('receipts.html')
from flask import Blueprint

eqname = Blueprint('eqname', __name__)

from . import views, forms, errors

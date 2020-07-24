from flask import Blueprint

eqde = Blueprint('eqde', __name__)

from . import views, forms, errors

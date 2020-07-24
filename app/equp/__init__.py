from flask import Blueprint

equp = Blueprint('equp', __name__)

from . import views, forms, errors

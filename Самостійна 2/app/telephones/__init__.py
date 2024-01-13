from flask import Blueprint

telephones_bp = Blueprint("telephones_bp", __name__, url_prefix='/telephones_bp')

from . import models
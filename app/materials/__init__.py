from flask import Blueprint

bp = Blueprint('materials', __name__)

from app.materials import routes
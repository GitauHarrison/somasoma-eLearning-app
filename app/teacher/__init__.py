from flask import Blueprint

bp = Blueprint('teacher', __name__)

from app.teacher import routes

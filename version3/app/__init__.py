from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootrstar = Bootstrap(app)

from app import routes, models, errors

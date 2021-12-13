from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

bootrstar = Bootstrap(app)

from app import routes, models, errors

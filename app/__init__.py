from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
from flask_pagedown import PageDown
from config import Config
from sqlalchemy import MetaData
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
bootstrap = Bootstrap()
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
moment = Moment()
mail = Mail()
pagedown = PageDown()

products = {
        'flask': {
            'name': 'Web Development with Flask and Python',
            'price': 3900,
        },
        'python-dsa': {
            'name': 'Python Data Structures and Algorithms',
            'price': 3900,
        },
        'data-science': {
            'name': 'Data Science with Python',
            'price': 7000,
        },
        'machine-learning': {
            'name': 'Machine Learning',
            'price': 7000,
        },
        'support': {
            'name': 'Python 1:1 support',
            'price': 10000,
            'per': 'hour',
            'adjustable_quantity': {
                'enabled': True,
                'minimum': 1,
                'maximum': 3
            },
        },
    }


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.student import bp as student_bp
    app.register_blueprint(student_bp, url_prefix='/student')

    from app.teacher import bp as teacher_bp
    app.register_blueprint(teacher_bp, url_prefix='/teacher')

    from app.materials import bp as materials_bp
    app.register_blueprint(materials_bp, url_prefix='/materials')

    if not app.debug and not app.testing:
        auth = None
        if app.config.get('MAIL_USERNAME') and app.config.get('MAIL_PASSWORD'):
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config.get('MAIL_USE_TLS'):
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'],
            subject='somasoma eLearning Failure',
            credentials=auth,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/somasoma.log',
            maxBytes=10240,
            backupCount=10
            )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('somasoma eLearning Startup')

    return app

from app import models

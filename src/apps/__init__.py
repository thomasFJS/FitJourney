"""
Author  :        Thomas Fujise
Date    :        08.04.2022
File    :        __init__.py
Version :        1.0.0
Brief   :        Application initialization
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_mail import Mail



db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def register_extensions(app):
    """
    Initialize extensions 

    - LoginManager
    - SQLAlchemy
    - FlaskMail
    """
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    """
    Register all blueprints
    """
    for module_name in ('authentication','client', 'coach'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def config_database(app):
    """
    Configure database 
    """
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def remove_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    config_database(app)
    return app
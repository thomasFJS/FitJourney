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

db = SQLAlchemy()
login_manager = LoginManager()

def register_blueprints(app):
    for module_name in ('')

def create_app(config):
    app = Flask(__name__)
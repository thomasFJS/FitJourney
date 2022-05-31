"""
Author  :        Thomas Fujise
Date    :        08.04.2022
File    :        config.py
Version :        1.0.0
Brief   :        Set the different config mode
"""

import os
from decouple import config

class Config(object):
    """
    Config parent class

    Contains all base config settings 
    """
    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = config('SECRET_KEY', default='S3cr3t_k3y')

    #Profile picture

    UPLOAD_FOLDER = config('UPLOAD_FOLDER', default='apps/static/assets/img/profile')

    DEFAULT_PROFILE_PIC = config('DEFAULT_PROFILE_PIC', default='default_profile_pic.png')

    #SQL ALCHEMY

    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='mysql+pymysql'),
        config('DB_USERNAME', default='fitjourney_dba'),
        config('DB_PASS', default='Super2012$'),
        config('DB_HOST', default='localhost'),
        config('DB_PORT', default='3306'),
        config('DB_NAME', default='fitjourney')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #FLASK MAIL
    MAIL_SERVER = config('MAIL_SERVER', default='smtp.gmail.com')
    MAIL_PORT = config('MAIL_PORT', default=465)
    MAIL_USERNAME = config('MAIL_USERNAME', default='fitjourney.cfpt@gmail.com')
    MAIL_PASSWORD = config('MAIL_PASSWORD', default='Super2012')
    MAIL_USE_TLS = config('MAIL_USE_TLS', default=False)
    MAIL_USE_SSL = config('MAIL_USE_SSL', default=True)
    MAIL_DEFAULT_SENDER = config('MAIL_DEFAULT_SENDER', default='fitjourney.cfpt@gmail.com')

class ProductionConfig(Config):
    """
    Production config class

    Contains all config settings for Production 
    """
    DEBUG = False

    #Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    """
    Debug config class

    Contains all config settings for Debug
    """
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}

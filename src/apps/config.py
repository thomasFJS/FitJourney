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
        config('DB_NAME', default='fitjourney2')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #FLASK MAIL
    MAIL_SERVER = config('MAIL_SERVER', default='smtp.mailtrap.io')
    MAIL_PORT = config('MAIL_PORT', default=2525)
    MAIL_USERNAME = config('MAIL_USERNAME', default='5806e099aa3376')
    MAIL_PASSWORD = config('MAIL_PASSWORD', default='c2857a008d8b60')
    MAIL_USE_TLS = config('MAIL_USE_TLS', default=True)
    MAIL_USE_SSL = config('MAIL_USE_SSL', default=False)
    MAIL_DEFAULT_SENDER = config('MAIL_DEFAULT_SENDER', default='thomas.fjs@eduge.ch')

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

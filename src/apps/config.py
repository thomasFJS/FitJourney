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

    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='mysql+pymysql'),
        config('DB_USERNAME', default=''),
        config('DB_PASS', default=''),
        config('DB_HOST', default='localhost'),
        config('DB_PORT', default='3306'),
        config('DB_NAME', default='')
    )


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

"""
Author  :        Thomas Fujise
Date    :        08.04.2022
File    :        run.py
Version :        1.0.0
Brief   :        Load the config mode and run the flask app
"""

from flask_migrate import Migrate 
from sys import exit
from decouple import config 

from apps.config import config_dict
from apps import create_app, db

# By default config set to debug mode
DEBUG = config('DEBUG', default=True, cast=bool)

#Get the config mode
config_mode = 'Debug' if DEBUG else 'Production'

try:
    app_config = config_dict[config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid config mode')

app = create_app(app_config)
Migrate(app,db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)

if __name__ == "__main__":
    app.run()
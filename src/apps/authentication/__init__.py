"""
Author  :        Thomas Fujise
Date    :        08.04.2022
File    :        __init__.py
Version :        1.0.0
Brief   :        Authentication blueprint initialization
"""

from flask import Blueprint


blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)
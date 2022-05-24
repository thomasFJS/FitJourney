"""
Author  :        Thomas Fujise
Date    :        08.04.2022
File    :        __init__.py
Version :        1.0.0
Brief   :        Coach blueprint initialization
"""

from flask import Blueprint

blueprint = Blueprint(
    'coach_blueprint',
    __name__,
    url_prefix=''
)
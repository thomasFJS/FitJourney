"""
Author  :        Thomas Fujise
Date    :        24.05.2022
File    :        forms.py
Version :        1.0.0
Brief   :        Coach forms 
"""

from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, PasswordField, IntegerField, BooleanField, ValidationError, SelectField, TextAreaField, HiddenField, PasswordField
from wtforms.validators import Email, DataRequired, EqualTo, Length
from wtforms.fields.html5 import DateField, EmailField, IntegerRangeField, TimeField
from wtforms.ext.dateutil.fields import DateTimeField
from datetime import datetime

class SessionForm(FlaskForm):
    """
    Create an adding session form
    """

    client = SelectField('Clients', id='clients_list', coerce=int)

    date = DateField('Date', id='datepick', validators=[DataRequired()])

    start_time = TimeField('Start Time', id="start_time", validators=[DataRequired()])

    end_time = TimeField('End Time', id="end_time", validators=[DataRequired()])

    duration = SelectField('Duration', id="duration", coerce=int)

    type = SelectField('Type', id="type_picker", coerce=int)

    add = SubmitField("Add")
"""
Author  :        Thomas Fujise
Date    :        24.05.2022
File    :        forms.py
Version :        1.0.0
Brief   :        Coach forms 
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import FileField, StringField, SubmitField, PasswordField, IntegerField, BooleanField, ValidationError, SelectField, TextAreaField, HiddenField, DecimalField
from wtforms.validators import Email, DataRequired, EqualTo, Length, Regexp
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

    duration = SelectField('Duration', id="duration", coerce=int, validators=[DataRequired()])

    type = SelectField('Type', id="type_picker", coerce=int)

    add = SubmitField("Add")

class AddClientForm(FlaskForm):
    """
    Create an adding client form
    """

    name = StringField('Name', id="name", validators=[DataRequired()])

    surname = StringField('Surname', id="surname", validators=[DataRequired()])

    email = EmailField('Email', id="email", validators=[DataRequired()])

    birthdate = DateField('Birthdate', id="birthdate", validators=[DataRequired()])

    height = IntegerField('Height', id="height", validators=[DataRequired()])

    start_date = DateField('Start date', id="start_date",  validators=[DataRequired()])

    subscription = SelectField('Subscription', id="subscription",  validators=[DataRequired()])

    end_date = DateField('End date', id="end_date",  validators=[DataRequired()])

    add = SubmitField("Add")


class ClientForm(FlaskForm):
    """
    Create a update form
    """

    name = StringField('Name', id='name', validators=[DataRequired()])

    surname = StringField('Surname', id='surname', validators=[DataRequired()])

    email = EmailField('Email', id="email", validators=[DataRequired(), Email()])

    birthdate = DateField('Birthdate', id="birthdate", validators=[DataRequired()])

    profile_pic = FileField('Profile Pic', id="profile_pic")

    card_id = IntegerField('Card ID', id='card_update')
    
    weight = StringField('Weight', id='weight_update')

    height = StringField('Height', id='height_update')

    subscriptionEnd = DateField('Subscription Until', id='subscription_until')

    address = StringField('Address', id='address')

    country = StringField('Country', id='country')

    city = StringField('City', id='city')

    npa = StringField('NPA', id='npa')

    register_date = DateField('Register date', id='register_date')

    change = SubmitField("Change")

    
class AddProgramForm(FlaskForm):
    """
    Create the adding program form
    """

    type = SelectField('Type', id="program_type",  validators=[DataRequired()], choices=[(1, "Diet"), (2, "Workout")])

    file = FileField('Program File', id="program_file", validators=[FileRequired(), FileAllowed(['pdf'], 'PDF only !')])

    client = HiddenField('Client', id="program_client")

    add = SubmitField("Upload")
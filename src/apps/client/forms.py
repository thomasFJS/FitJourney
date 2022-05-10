"""
Author  :        Thomas Fujise
Date    :        12.04.2022
File    :        forms.py
Version :        1.0.0
Brief   :        Client forms 
"""

from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, PasswordField, IntegerField, BooleanField, ValidationError
from wtforms.validators import Email, DataRequired, EqualTo, Length
from wtforms.fields.html5 import DateField, EmailField


class UpdateForm(FlaskForm):
    """
    Create a update form
    """

    name = StringField('Name', id='name_update', validators=[DataRequired()])

    surname = StringField('Surname', id='surname_update', validators=[DataRequired()])

    email = EmailField('Email', id="email_update", validators=[DataRequired(), Email()])

    birthdate = DateField('Birthdate', id="birthdate_update", validators=[DataRequired()])

    profile_pic = FileField('Profile Pic', id="profile_pic_update")

    card_id = IntegerField('Card ID', id='card_update')
    
    weight = StringField('Weight', id='weight_update')

    height = StringField('Height', id='height_update')

    subscriptionEnd = DateField('Subscription Until', id='subscription_until')

    address = StringField('Address', id='address_update')

    country = StringField('Country', id='country_update')

    city = StringField('City', id='city_update')

    npa = StringField('NPA', id='npa_update')

    update = SubmitField("Update")
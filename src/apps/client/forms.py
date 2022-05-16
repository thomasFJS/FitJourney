"""
Author  :        Thomas Fujise
Date    :        12.04.2022
File    :        forms.py
Version :        1.0.0
Brief   :        Client forms 
"""

from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, PasswordField, IntegerField, BooleanField, ValidationError, SelectField, TextAreaField
from wtforms.validators import Email, DataRequired, EqualTo, Length
from wtforms.fields.html5 import DateField, EmailField, IntegerRangeField


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


class AddReviewForm(FlaskForm):
    """
    Create form to add review 
    """

    Field1 = IntegerRangeField('Field1', id='Field1', default=0)

    Field2 = IntegerRangeField('Field2', id='Field2', default=0)

    Field3 = IntegerRangeField('Field3', id='Field3', default=0)

    Field4 = IntegerRangeField('Field4', id='Field4', default=0)

    Comment = TextAreaField('Comment', id='Comment')

    Submit = SubmitField("Submit")
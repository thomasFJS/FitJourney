"""
Author  :        Thomas Fujise
Date    :        12.04.2022
File    :        forms.py
Version :        1.0.0
Brief   :        Client forms 
"""

from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, PasswordField, IntegerField, BooleanField, ValidationError, SelectField, TextAreaField, HiddenField, PasswordField
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

    field1 = IntegerRangeField('Field1', id='field1', default=0)

    field2 = IntegerRangeField('Field2', id='field2', default=0)

    field3 = IntegerRangeField('Field3', id='field3', default=0)

    field4 = IntegerRangeField('Field4', id='field4', default=0)

    comment = TextAreaField('Comment', id='comment')
    
    type = HiddenField('Type', id='type')

    target = HiddenField('Target', id='target')

    submit = SubmitField("Submit")

class ChangePasswordForm(FlaskForm):
    """
    Create form to change password
    """

    oldPassword = PasswordField('Old Password', id='oldPassword')

    newPassword = PasswordField('New Password', id='newPassword')

    confirmPassword = PasswordField('Confirm New Password', id='confirmPassword')
    
    change = SubmitField("Change")
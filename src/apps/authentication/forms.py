"""
Author  :        Thomas Fujise
Date    :        12.04.2022
File    :        forms.py
Version :        1.0.0
Brief   :        Authentication forms 
"""

from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, PasswordField, IntegerField, BooleanField, ValidationError
from wtforms.validators import Email, DataRequired, EqualTo, Length
from wtforms.fields.html5 import DateField, EmailField


class LoginForm(FlaskForm):
    """
    Create a login form
    """
    email = StringField('email', id='email_login', validators=[DataRequired()])

    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])
    
    login = SubmitField("login")

class RegisterForm(FlaskForm):
    """
    Create a register form
    """ 
    name = StringField('Name', id='name_register', validators=[DataRequired()])

    surname = StringField('Surname', id='surname_register', validators=[DataRequired()])

    email = EmailField('Email', id="email_rgister", validators=[DataRequired(), Email()])

    birthdate = DateField('Birthdate', id="date_register", validators=[DataRequired()])

    password = PasswordField('Password', id='password_register', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords Must Match!')])

    confirm_password = PasswordField('Confirm Password', id='password2_register')

    register = SubmitField("register")


class UpdateForm(FlaskForm):
    """
    Create a update form
    """

    name = StringField('Name', id='name_update', validators=[DataRequired()])

    surname = StringField('Surname', id='surname_update', validators=[DataRequired()])

    email = EmailField('Email', id="email_update", validators=[DataRequired(), Email()])

    birthdate = DateField('Birthdate', id="birthdate_update", validators=[DataRequired()])

    profile_pic = FileField('Profile Pic', id="profile_pic_update")

    card_id = IntegerField()

    address = StringField('Address', id='address_update')

    country = StringField('Country', id='country_update')

    city = StringField('City', id='city_update')

    npa = StringField('NPA', id='npa_update')

    update = SubmitField("Update")
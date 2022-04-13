"""
Author  :        Thomas Fujise
Date    :        12.04.2022
File    :        forms.py
Version :        1.0.0
Brief   :        Authentication forms 
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, BooleanField, ValidationError
from wtforms.validators import Email, DataRequired, EqualTo, Length


class LoginForm(FlaskForm):
    """
    Create a login form
    """
    email = StringField('email', id='email_login', validators=[DataRequired()])

    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])
    
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    """
    Create a register form
    """ 
    username = StringField('Userame', id='name_register', validators=[DataRequired()])

    surname = StringField('Surname', id='surname_register', validators=[DataRequired()])

    email = StringField('Email', id="email_rgister", validators=[DataRequired(), Email()])

    birthdate = DateField('Birthdate', id="date_register", validators=[DataRequired()])

    password = PasswordField('Password', id='password_register', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords Must Match!')])

    confirm_password = PasswordField('Confirm Password', id='password2_register', validators=[DataRequired()])


"""
Author  :        Thomas Fujise
Date    :        11.04.2022
File    :        routes.py
Version :        1.0.0
Brief   :        Set all authentication routes
"""

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, RegisterForm
from apps.authentication.models import Users
from apps.authentication.util import verify_pass



@blueprint.route('/')
def route_default():
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if 'login' in request.form:

        #read form data
        email = request.form['email']
        password = request.form['password']

        #Locate the user
        user = Users.query.filter_by(email=email).first()

        #Check password
        if user and verify_pass(password, user.password):
            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something is not ok (user or password)
        return render_template('accounts/login.html', msg='Wrong user or password', form=login_form)
    
    if not current_user.is_authenticated:
        return render_template('accounts/login.html',form=login_form)
    
    return redirect(url_for('home_blueprint.index'))
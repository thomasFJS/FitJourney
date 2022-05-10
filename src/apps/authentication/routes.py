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
from apps.authentication.models import User
from apps.authentication.util import verify_pass


#Default route
@blueprint.route('/')
def route_default():
    return redirect(url_for('client_blueprint.index'))


#Login route
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Display login page with the login form 
    """
    login_form = LoginForm()
    if login_form.validate_on_submit():

        #read form data
        email = request.form['email']
        password = request.form['password']

        #Locate the user
        user = User.query.filter_by(email=email).first()
        #Check password
        if user and verify_pass(password, user.password):
            
            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something is not ok (user or password)
        return render_template('accounts/login.html', msg='Wrong user or password', form=login_form)
    
    if not current_user.is_authenticated:
        return render_template('accounts/login.html',form=login_form)
    
    return redirect(url_for('home_blueprint.index'))


#Register route
@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    Display Register page with the register form 
    """
    register_form = RegisterForm()

    if register_form.validate_on_submit():

        email = request.form['email']
        #name = request.form['name']

        #Check if user already exists
        user = User.query.filter_by(email=email).first()

        if user:
            return render_template('accounts/register.html', msg='Email Already registered', success=False, form=register_form)

        #Else we create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html', msg='User has been created please <a href="/login"> login</a> ', success=True, form=register_form)

    else:
        return render_template('accounts/register.html', form=register_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

"""
Author  :        Thomas Fujise
Date    :        11.04.2022
File    :        routes.py
Version :        1.0.0
Brief   :        Set all authentication routes
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask_login import login_required

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, RegisterForm
from apps.authentication.models import User
from apps.authentication.util import verify_pass



#Default route
@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


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
        flash('Wrong user or password', 'danger')
        return redirect(url_for('authentication_blueprint.route_default', msg='Wrong user or password'))

    if not current_user.is_authenticated:
        
        return render_template('accounts/login.html',form=login_form)
    
    if current_user.role  == 1:
        #CLIENT
        return redirect(url_for('client_blueprint.index'))
    elif current_user.role == 2:
        #COACH
        return redirect(url_for('coach_blueprint.dashboard'))

    return redirect(url_for('client_blueprint.index'))


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
            flash("Email already registered", 'warning')
            return render_template('accounts/register.html', msg='Email Already registered', success=False, form=register_form)


         #try to create the user
        try:
            user = User(name=request.form['name'], surname=request.form['surname'], email=request.form['email'], birthdate=request.form['birthdate'], password=request.form['password'], role=2)
            db.session.add(user)
            db.session.commit()
            flash("User has been created please login", 'success')
            return redirect(url_for('authentication_blueprint.login'))
        except:
            db.session.rollback()
            flash("Error while registering new user", 'danger')
            return redirect(url_for('authentication_blueprint.register'))



        return render_template('accounts/register.html', msg='<a href="/login"> LOGIN</a> ', success=True, form=register_form)

    else:
        return render_template('accounts/register.html', form=register_form)


@blueprint.route('/logout')
@login_required
def logout():

    logout_user()   

    return redirect(url_for('authentication_blueprint.login'))

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page-500.html'), 500

"""
Author  :        Thomas Fujise
Date    :        23.05.2022
File    :        routes.py
Version :        1.0.0
Brief   :        Set all the coach routes
"""

# APP
from apps.coach import blueprint
from apps import db, login_manager
from apps.authentication.models import User, PhysicalInfo, Subscription, CoachingReview, WorkoutReview, Review, Workout, WorkoutType, Session
from apps.coach.forms import SessionForm, AddClientForm, ClientForm
from apps.config import Config

# FLASK
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from jinja2 import TemplateNotFound

from flask_login import (
    current_user
)

# UTILS
import uuid as uuid
import os
from werkzeug.utils import secure_filename
from datetime import date, datetime

from apps.coach.util import *
from apps.client.util import *

@blueprint.route('/dashboard')
@login_required
def dashboard():

    nextClient = get_coach_next_session(current_user.id)
    clientLastWorkout = get_last_workout(nextClient.id) if nextClient != None else None

    clients = get_clients(current_user.id)
    return render_template('coach/dashboard.html', segment='coach_dashboard', nextClient=nextClient, clientLastWorkout=clientLastWorkout, clients=clients)


@blueprint.route('/calendar', methods=['POST', 'GET'])
@login_required
def calendar():
    form = SessionForm(request.form)
    # Set select input choices
    form.client.choices = [(client['id'], str(client['name'] + " " + client['surname'])) for client in get_clients(current_user.id)]
    form.duration.choices = [(i,i) for i in range(1,4)]
    form.type.choices = [(type.id, type.title) for type in get_all_workout_types()]

    sessions = get_sessions(current_user.id)
    print(sessions)

    if request.method == 'POST':
        startDate = request.form['date']
        startTime = request.form['start_time']
        endTime = request.form['end_time']

        # Set datetime value
        startDateTime = datetime.strptime(startDate + " " + startTime, '%Y-%m-%d %H:%M')
        endDateTime = datetime.strptime(startDate + " " + endTime, '%Y-%m-%d %H:%M:%S')
        try :
            newSession = Session(start_time=startDateTime, end_time=endDateTime, duration=request.form['duration'], workout_type=request.form['type'], client_id=request.form['client'], coach_id=current_user.id)
            db.session.add(newSession)
            db.session.commit()
            flash("The session is registered !", 'success')
            return redirect( url_for('coach_blueprint.calendar') )
        except:
            db.session.rollback()
            flash("Error while trying to add a new session, please try again", 'danger')
            return redirect( url_for('coach_blueprint.calendar') )
        
    return render_template('coach/calendar.html', form=form, sessions=sessions)

@blueprint.route('/client', methods=['POST', 'GET'])
@login_required
def client():
    form = ClientForm(request.form)
    client_id = request.args.get('clientId')

    reviews = get_reviews(client_id)
    clientDetails = get_client_details(client_id)
    subscriptionUntil = get_subscription_end_date(client_id)
    physicalInfo = get_physical_infos(client_id)

    # Get each workout type and how many client have made in 2 separate array to use them in js
    wrktTypeList = get_workout_type_count(client_id)[0]
    wrktTypeCount = get_workout_type_count(client_id)[1]

    nbWorkoutPerMonth = get_workout_count_per_month(client_id)
    
    return render_template('coach/client.html', segment='client', form=form, reviews=reviews, client=clientDetails, subscriptionUntil=subscriptionUntil,
     wrktTypeCount=wrktTypeCount, wrktTypeList=wrktTypeList, nbWorkoutPerMonth=nbWorkoutPerMonth)


@blueprint.route('/add_client', methods=['POST', 'GET'])
@login_required
def add_client():
    form = AddClientForm(request.form)

    form.subscription.choices = [(subscription.duration, subscription.title + " - " + str(subscription.cost) + "CHF") for subscription in get_all_subscriptions()]

    if request.method == 'POST':
        print(request.form)
        height = request.form['height']
        surname = request.form['surname']
        email = request.form['email']
        name = request.form['name']
        birthdate = request.form['birthdate']
        date = request.form['start_date']
        end_date = request.form['end_date']
        subscription = request.form['subscription']
        
        try:
            newClient = User(name=name,surname=surname, email=email, birthdate=birthdate, profile_pic=Config.DEFAULT_PROFILE_PIC,role=1, password=name+"123")
            db.session.add(newClient)
            db.session.flush()
            print(newClient.id)
            newCoachAssign = CoachedBy(client_id=newClient.id, coach_id=current_user.id, starting_date=date, end_date=end_date)
            newPurchase = Purchase(client_id=newClient.id, date=date, subscription_id=get_subscription_id(subscription).id)
            db.session.add(newPurchase)
            db.session.add(newCoachAssign)
            db.session.commit()
            flash("New client is registered !", 'success')
            return redirect( url_for('coach_blueprint.dashboard') )
        except:
            db.session.rollback()
            flash("Error, while trying to register new client, please try again", 'danger')
            return redirect(url_for('coach_blueprint.dashboard'))


    return render_template('coach/add_client.html', segment='add_client', form=form) 
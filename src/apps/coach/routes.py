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
from apps.coach.forms import SessionForm
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


    if request.method == 'POST':
        print(request.form['client'])
        newSession = Session(date=request.form['date'], duration='', workout_type='')
    return render_template('coach/calendar.html', form=form)
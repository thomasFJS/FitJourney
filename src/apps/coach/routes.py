"""
Author  :        Thomas Fujise
Date    :        23.05.2022
File    :        routes.py
Version :        1.0.0
Brief   :        Set all the coach routes
"""

# APP
from apps.client import blueprint
from apps import db, login_manager
from apps.authentication.models import User, PhysicalInfo, Subscription, CoachingReview, WorkoutReview, Review, Workout, WorkoutType, Session
from apps.client.forms import UpdateForm, AddReviewForm, ChangePasswordForm
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
def coach_dashboard():

    nextClient = get_coach_next_session(current_user.id)
    clientLastWorkout = get_last_workout(nextClient.id)

    clients = get_clients(current_user.id)
    return render_template('coach/dashboard.html', segment='coach_dashboard', nextClient=nextClient, clientLastWorkout=clientLastWorkout, clients=clients)
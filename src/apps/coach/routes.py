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
from apps.authentication.models import User, PhysicalInfo, Subscription, CoachingReview, WorkoutReview, Review, Workout, WorkoutType, Session, Program, CoachedBy, Purchase
from apps.coach.forms import SessionForm, AddClientForm, ClientForm, AddProgramForm, AddCheckUpForm, RenewSubscriptionForm
from apps.config import Config

# FLASK
from flask import render_template, redirect, request, url_for, flash, send_file
from flask_login import login_required
from jinja2 import TemplateNotFound

from flask_login import (
    current_user
)

# UTILS
from io import BytesIO
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
    #print(sessions)

    if request.method == 'POST':
        #Check if client there is client in the select field
        if 'client' not in request.form:
            flash("You don't have client to select, please add a client before", 'danger')
            return redirect( url_for('coach_blueprint.calendar') )

        startDate = request.form['date']
        startTime = request.form['start_time']
        endTime = request.form['end_time']
        durationSelected = request.form['duration']

        # Set datetime value
        startDateTime = datetime.strptime(startDate + " " + startTime, '%Y-%m-%d %H:%M')
        endDateTime = datetime.strptime(startDate + " " + endTime, '%Y-%m-%d %H:%M:%S')

        # Set duration format
        duration = "0{durationSelected}:00:00".format(durationSelected=durationSelected)

        try :
            newSession = Session(start_time=startDateTime, end_time=endDateTime, duration=duration, workout_type=request.form['type'], client_id=request.form['client'], coach_id=current_user.id)
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
    #Get client id
    client_id = request.args.get('clientId')

    #Get client infos to display
    reviews = get_reviews(client_id)
    clientDetails = get_client_details(client_id)
    subscriptionUntil = get_subscription_end_date(client_id)
    physicalInfo = get_physical_infos(client_id)

    # Get each workout type and how many client have made in 2 separate array to use them in js
    wrktTypeList = get_workout_type_count(client_id)[0]
    wrktTypeCount = get_workout_type_count(client_id)[1] if get_workout_type_count(client_id)[1] != [] else 0

    nbWorkoutPerMonth = get_workout_count_per_month(client_id)

    programs = get_program(client_id)
    workoutProgram = programs[0]
    dietProgram = programs[1]

    # Get the average of heart rate during this week
    avgHeartRate = get_average_heart_rate_last_week(client_id)
	# Get the average of calories burned this week
    avgCalories = get_average_calories_last_week(client_id)

    return render_template('coach/client.html', segment='client', form=form, reviews=reviews, client=clientDetails, subscriptionUntil=subscriptionUntil,
     wrktTypeCount=wrktTypeCount, wrktTypeList=wrktTypeList, nbWorkoutPerMonth=nbWorkoutPerMonth, workoutProgram=workoutProgram, dietProgram=dietProgram, physicalInfo=physicalInfo,
     avgCalories=avgCalories, avgHeartRate=avgHeartRate)


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
            print(get_subscription_id(subscription).id)
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

@blueprint.route('/add_program', methods=['POST', 'GET'])
@login_required
def add_program():
    form=AddProgramForm()
    #Get client id
    client_id = request.args.get('clientId')
  
    if request.method == "POST":
        if form.validate_on_submit():
            
            file_name = form.file.data
            try:
                newProgram = Program(type=request.form['type'], pdf=file_name.read(),date=date.today(), client_id=request.form['client'], coach_id=current_user.id)
                db.session.add(newProgram)
                db.session.commit()
                flash("Program Added !", 'success')
                return redirect(url_for('coach_blueprint.client', clientId=request.form['client']))
            except:
                db.session.rollback()
                flash("Error while adding the new program", 'danger')
                return redirect(url_for('coach_blueprint.client', clientId=request.form['client']))
            
    return render_template('coach/add_program.html', segment='add_program', form=form, clientId=client_id)


@blueprint.route('/program', methods=['GET'])
@login_required
def program():

    program_id = request.args.get('programId')
    program_type = request.args.get('programType')

    program = get_program_by_id(program_id)

    return send_file(BytesIO(program.pdf), attachment_filename=str(program_type+'.pdf'), as_attachment=True)
    

@blueprint.route('/check_up', methods=['POST', 'GET'])
@login_required
def check_up():
    form = AddCheckUpForm(request.form)
    client_id = request.args.get('clientId')

    # Get the client details
    infos = get_client_details(client_id)
    today = date.today()
    # Set the static infos for the check up forms
    static_infos = {
        "id" : infos.id,
        "name" : infos.name,
        "surname" : infos.surname,
        "age" : (today.year - infos.birthdate.year - ((today.month, today.day) < (infos.birthdate.month, infos.birthdate.day))) #Get age with birthdate and date.today()
    }

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                newCheckup = PhysicalInfo(user_id=client_id, height=request.form['height'], weight=request.form['weight'], age=request.form['age'],
                    bmi=request.form['bmi'], bmr=request.form['bmr'], bodyfat_percentage=request.form['body_fat_percent'], muscle_mass_percentage=request.form['muscle_mass_percent'],
                    bone_mass_percentage=request.form['bone_mass_percent'], water_percentage=request.form['water'], protein_percentage=request.form['protein'], 
                    bone_mass=request.form['bone_mass'], muscle_mass=request.form['muscle_mass'], bodyfat_mass=request.form['body_fat'], leanbody_mass=request.form['lean_body_mass'],
                    fat_visceral=request.form['fat_visceral'], body_age=request.form['body_age'], date=today)
                db.session.add(newCheckup)
                db.session.commit()
                flash("Check up added !", 'success')
                return redirect(url_for('coach_blueprint.client', clientId=client_id))
            except:
                flash("Error while trying to add check up", 'danger')
                return redirect(url_for('coach_blueprint.client', clientId=client_id))

    return render_template('coach/add_checkup.html', segment='add_checkup', form=form, infos=static_infos)

@blueprint.route('/new_subscription', methods=['POST', 'GET'])
@login_required
def new_subscription():
    form=RenewSubscriptionForm(request.form)

    #Set the subscription choices
    form.subscription.choices = [(subscription.duration, subscription.title + " - " + str(subscription.cost) + "CHF") for subscription in get_all_subscriptions()]

    client_id = request.args.get('clientId')
    # Get the client details
    client = get_client_details(client_id)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                print(get_subscription_id(request.form['subscription']).id)
                newCoachAssign = CoachedBy(client_id=client_id, coach_id=current_user.id, starting_date=request.form['start_date'], end_date=request.form['end_date'])
                newPurchase = Purchase(client_id=client_id, date=request.form['start_date'], subscription_id=get_subscription_id(request.form['subscription']).id)
                print("OK")
                db.session.add(newPurchase)
                db.session.add(newCoachAssign)
                db.session.commit()
                flash("New subscription is purchased !", 'success')
                return redirect( url_for('coach_blueprint.client', clientId=client_id) )
            except:
                db.session.rollback()
                flash("Error, while trying to purchase new subscription", 'danger')
                return redirect(url_for('coach_blueprint.client', clientId=client_id))

    return render_template('coach/new_subscription.html', segment='new_subscription', form=form, client=client)
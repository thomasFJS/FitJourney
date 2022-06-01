"""
Author  :        Thomas Fujise
Date    :        11.04.2022
File    :        routes.py
Version :        1.0.0
Brief   :        Set all the client routes
"""

# APP
from apps.client import blueprint
from apps import db, login_manager
from apps.authentication.models import User, PhysicalInfo, Subscription, CoachingReview, WorkoutReview, Review, Workout, WorkoutType, Session
from apps.client.forms import UpdateForm, AddReviewForm, ChangePasswordForm
from apps.config import Config
from apps.authentication.util import verify_pass, hash_pass

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

from apps.client.util import *
from apps.coach.util import get_program

@blueprint.route('/index')
@login_required
def index():
	nextSessions = get_next_session(current_user.id)
	return render_template('client/index.html', segment='index', nextSessions=nextSessions)

# Create Profile Page
@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	update_form = UpdateForm(request.form)
	# Get the last physical information of the user
	physicalInfo = get_physical_infos(current_user.id)

	# Get the reviews posted by user
	reviews = get_reviews(current_user.id)

	# Get each workout type and how many client have made in 2 separate array to use them in js
	wrktTypeList = get_workout_type_count(current_user.id)[0]

	wrktTypeCount = get_workout_type_count(current_user.id)[1] if get_workout_type_count(current_user.id)[1] != [] else 0

	# Get the number of workout per month during this year
	nbWorkoutPerMonth = get_workout_count_per_month(current_user.id)
	
	# Get the average of heart rate during this week
	avgHeartRate = get_average_heart_rate_last_week(current_user.id)

	# Get the average of calories burned this week
	avgCalories = get_average_calories_last_week(current_user.id)
	# Get the total time training this week
	totalTime = get_time_working_out_last_week(current_user.id)

	# Get the average weight recorded for each month
	weightUpdate = get_weight_update(current_user.id)

	#Get the latest programs 
	programs = get_program(current_user.id)

	# Get Coaching review fields name 
	coachingReviewFields = get_coaching_review_field() 

	# Get coach id 
	coachId =get_actual_coach_id(current_user.id)

	#set the programs
	current_user.workoutProgram = programs[0]
	current_user.dietProgram = programs[1]

	# Set the average heartRate for all workout made this week
	current_user.avgHeartRate = avgHeartRate

	# Set the average heartRate for all workout made this week
	current_user.avgCalories = avgCalories

	# Set the total time of working out this week
	current_user.totalTime = totalTime

	# Set the number of workout per month
	current_user.nbWorkoutPerMonth = nbWorkoutPerMonth

	# Set the average weight per month
	current_user.weightUpdate = weightUpdate

	# Set the 2 array for workout type
	current_user.workoutTypeList = wrktTypeList
	current_user.workoutTypeCount = wrktTypeCount

	#Set all the reviews
	current_user.reviews = reviews

	# Set the physical value to the user
	current_user.physicalInfo = physicalInfo

	# Get last subscription end date
	current_user.subscriptionEnd = get_subscription_end_date(current_user.id)

	if request.method == "POST":
		current_user.name = request.form['name']
		current_user.surname = request.form['surname']
		current_user.email = request.form['email']
		current_user.birthdate = request.form['birthdate']
		current_user.address = request.form['address']
		current_user.city = request.form['city']
		current_user.country = request.form['country']
		current_user.npa = request.form['npa']

		# Check if new profile pic
		if request.files['profile_pic']:
			current_user.profile_pic = request.files['profile_pic']
			# Grab Image name
			pic_filename = secure_filename(current_user.profile_pic.filename)
			pic_name = str(uuid.uuid1()) + "_" + pic_filename

			saver = request.files['profile_pic']

			# Change it to a string to save to db
			current_user.profile_pic = pic_name

			try:
				db.session.commit()
				saver.save(os.path.join(Config.UPLOAD_FOLDER, pic_name))
				flash("Account Updated successfully !", 'success')
				return render_template("client/profile.html",
						form=update_form,
						reviewFields=coachingReviewFields,
						reviewTargetId=coachId
				)		
			except:
				flash("Error! Looks like there was a problem.. try again!", 'danger')
				return render_template("client/profile.html",
						form=update_form,
						reviewFields=coachingReviewFields,
						reviewTargetId=coachId
						)
		else:
			db.session.commit()
			flash("User Updated successfully !", 'success')
			return render_template("client/profile.html", 
					form=update_form,
					reviewFields=coachingReviewFields,
					reviewTargetId=coachId
					)
	else:
		return render_template("client/profile.html", segment='profile',
				form=update_form,
				id = id,
				physicalInfo=physicalInfo,
				reviewFields=coachingReviewFields,
				reviewTargetId=coachId)

	return render_template("client/profile.html", segment='profile')


@blueprint.route('/review/', methods=['GET'])
@login_required
def review():	
	# Put all parameters into dict 
	reviewDetails = request.args.to_dict()
	review = get_review_details(reviewDetails['Id'], reviewDetails['Type'])[0]
	# Client who post the review
	client = get_review_author(review.id_client)

	# Target of the review may be workout or a coach depends on review type
	target = get_review_details(reviewDetails['Id'], reviewDetails['Type'])[1]

	return render_template('client/review.html', segment='review', review=review, client=client, target=target)

# Create Workouts Page
@blueprint.route('/workouts')
@login_required
def workouts():
	# Get all data from workout 
	#workouts = db.session.query(WorkoutType.title, WorkoutType.logo,Workout.id, Workout.date, Workout.duration, Workout.heart_rate_max, Workout.heart_rate_min, 
	#			Workout.heart_rate_avg, Workout.calories, Workout.active_calories, Workout.distance, Workout.pace_avg).join(WorkoutType, Workout.workout_type == WorkoutType.id).filter(Workout.client_id==id).order_by(Workout.date.desc())
	workouts = get_workouts(current_user.id)
	return render_template('client/workouts.html', segment='workouts', workouts=workouts)


@blueprint.route('/workout')
@login_required
def workout():
	# put all parameters into dict 
	params = request.args.to_dict()

	workoutDetails = get_workout_details(params['Id'])

	workoutReview = get_workout_review_field()

	return render_template('client/workout.html', segment="workout", workoutDetails=workoutDetails, workoutReview=workoutReview)

@blueprint.route('/add_review', methods=['POST', 'GET'])
@login_required
def add_review():
	add_review_form = AddReviewForm(request.form)

	# put all parameters into dict 
	reviewFields = request.args.to_dict()
	print(reviewFields)
	if request.method == 'POST':
		newReview = Review(comment=request.form['comment'], date=datetime.now(),type=request.form['type'],id_client=current_user.id)
		db.session.add(newReview)	
		db.session.flush()
		if request.form['type'] == "WORKOUT":
			exists = is_workout_reviewed(request.form['target'])
			if exists :
				db.session.rollback()
				flash("You already add a review on this workout", 'warning')
				return redirect( url_for('client_blueprint.workouts') )
			else :
				# Try to add and commit the workout review 
				try:
					newWorkoutReview = WorkoutReview(id= newReview.id,difficulty=request.form['field1'], feel=request.form['field2'], fatigue=request.form['field3'], energy=request.form['field4'], target_id=request.form['target'])
					db.session.add(newWorkoutReview)
					db.session.commit()
					flash("Your workout review is added", 'success')
				except :
					db.session.rollback()
					flash("Error, please try again", 'danger')
				
				return redirect( url_for('client_blueprint.workouts') )

		elif request.form['type'] == "COACHING" :
			
			# Try to add and commit the coaching review 
			try:
				newCoachingReview = CoachingReview(id=newReview.id,satisfaction=request.form['field1'], support=request.form['field2'], disponibility=request.form['field3'], advice=request.form['field4'], target_id=request.form['target'])
				db.session.add(newCoachingReview)
				db.session.commit()
				flash("Your coaching review is added", 'success')
			except:
				flash("Error, please try again", 'danger')

			
			return redirect( url_for('client_blueprint.profile') )
		
		
	return render_template('client/add_review.html', segment="add_review", form=add_review_form, reviewFields=reviewFields)


@blueprint.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
	form = ChangePasswordForm(request.form)

	if request.method == 'POST':
		# Check if the old password is correct
		if verify_pass(request.form['oldPassword'], current_user.password):
			# Check if the confirmation field match the new password
			if request.form['newPassword'] == request.form['confirmPassword'] and request.form['newPassword'] != None:

				try:
					# Set the new password
					current_user.password = hash_pass(request.form['newPassword'])
					db.session.flush()
					db.session.commit()
					flash("Password updated", 'success')
					return redirect( url_for('client_blueprint.profile') )
				except: 
					flash("Error, please try again", 'danger')
			else :
				flash ("Passwords must match !", 'warning')
		else:
			flash("Old password isn't correct !", 'warning')
	return render_template('client/change_password.html', segment="change_password", form=form)


# Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment
    except: 
        return None
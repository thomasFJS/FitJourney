"""
Author  :        Thomas Fujise
Date    :        11.04.2022
File    :        routes.py
Version :        1.0.0
Brief   :        Set all the application routes
"""

# APP
from apps.client import blueprint
from apps import db, login_manager
from apps.authentication.models import User, PhysicalInfo, Subscription, Purchase, CoachingReview, SessionReview, Review, Workout, WorkoutType, Session
from apps.client.forms import UpdateForm
from apps.config import Config

# FLASK
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from jinja2 import TemplateNotFound

from flask_login import (
    current_user
)

# SQL ALCHEMY 
from sqlalchemy import union

# UTILS
from dateutil.relativedelta import relativedelta
import uuid as uuid
import os
from werkzeug.utils import secure_filename

@blueprint.route('/index')
@login_required
def index():
    return render_template('client/index.html', segment='index')

# Create Profile Page
@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	update_form = UpdateForm(request.form)
	id = current_user.id
	user = User.query.get_or_404(id)

	# SQL request to get the last physical information of the user

	# SELECT * 
	# FROM `PHYSICAL_INFO`
	# WHERE `PHYSICAL_INFO`.USER_ID = %(CLIENT_ID_1)S
	# ORDER BY `PHYSICAL_INFO`.DATE
	physicalInfo = PhysicalInfo.query.filter_by(user_id=id).order_by(PhysicalInfo.date).first()

	# SQL Request to get the last subsciption purchase date and the duration of the subscription purchased
	#
	# SELECT `SUBSCRIPTION`.DURATION AS `SUBSCRIPTION_DURATION`, `PURCHASE`.DATE AS `PURCHASE_DATE` 
	# FROM `PURCHASE` 
	# INNER JOIN `SUBSCRIPTION` ON `PURCHASE`.SUBSCRIPTION_ID = `SUBSCRIPTION`.ID 
	# WHERE `PURCHASE`.CLIENT_ID = %(CLIENT_ID_1)S 
	# ORDER BY `PURCHASE`.DATE

	subscription = db.session.query(Subscription.duration, Purchase.date).join(Subscription, Purchase.subscription_id==Subscription.id).filter(Purchase.client_id==id).order_by(Purchase.date).first()
	
	#Queries to get all Review from user 
	coachingReview = db.session.query(CoachingReview.id, CoachingReview.satisfaction.label("Field1"), CoachingReview.support.label("Field2"), CoachingReview.disponibility.label("Field3"), CoachingReview.advice.label("Field4"), CoachingReview.target_id.label("target_id"))
	sessionReview = db.session.query(SessionReview.id, SessionReview.difficulty, SessionReview.feel, SessionReview.fatigue, SessionReview.energy, SessionReview.target_id)

	#UNION with the 2 queries 
	reviewsUnion = union(coachingReview,sessionReview).alias()

	#q4 = aliased(q3, name="If")

	query = db.session.query(Review.id, Review.comment, Review.date, Review.type, reviewsUnion.c.Field1, reviewsUnion.c.Field2, reviewsUnion.c.Field3, reviewsUnion.c.Field4, Review.id_client, reviewsUnion.c.target_id).select_from(reviewsUnion).join(Review,Review.id==reviewsUnion.c.COACHING_REVIEW_id).filter(Review.id_client==id).order_by(Review.date.desc())


	#Set all the reviews
	current_user.reviews = query

	# Set the physical value to the user
	current_user.physicalInfo = physicalInfo

	#Define subscription end date by adding the duration of the subscription in months to the purchase date.
	current_user.subscriptionEnd = (subscription[1] + relativedelta(months=subscription[0])).date()

	if request.method == "POST":
		user.name = request.form['name']
		user.surname = request.form['surname']
		user.email = request.form['email']
		user.birthdate = request.form['birthdate']
		user.address = request.form['address']
		user.city = request.form['city']
		user.country = request.form['country']
		user.npa = request.form['npa']

		# Check if new profile pic
		if request.files['profile_pic']:
			user.profile_pic = request.files['profile_pic']

			# Grab Image name
			pic_filename = secure_filename(user.profile_pic.filename)
			pic_name = str(uuid.uuid1()) + "_" + pic_filename

			saver = request.files['profile_pic']

			# Change it to a string to save to db
			user.profile_pic = pic_name


			try:
				db.session.commit()
				saver.save(os.path.join(Config.UPLOAD_FOLDER, pic_name))
				flash("Account Updated successfully !")
				return render_template("client/profile.html",
						form=update_form
				)		
			except:
				flash("Error! Looks like there was a problem.. try again!")
				return render_template("client/profile.html",
						form=update_form
						)
		else:
			db.session.commit()
			flash("User Updated successfully !")
			return render_template("client/profile.html", 
					form=update_form
					)
	else:
		return render_template("client/profile.html", segment='profile',
				form=update_form,
				id = id,
				physicalInfo=physicalInfo)

	return render_template("client/profile.html", segment='profile')


@blueprint.route('/review/', methods=['GET'])
@login_required
def review():	

	# Put all parameters into dict 
	reviewDetails = request.args.to_dict()

	# Client who post the review
	client = db.session.query(User.name, User.surname).filter(User.id==reviewDetails['Client']).first()

	target = {}
	# Target of the review may be session or a coach depends on review type
	if reviewDetails['Type'] == "SESSION":
		targetQuery = db.session.query(WorkoutType.title, Session.date, Session.time, Session.duration).join(WorkoutType, WorkoutType.id==Session.workout_type).filter(Session.id==reviewDetails['Target']).first()
		target['Type'] = targetQuery.title
		target['Date'] = targetQuery.date
		target['Time'] = targetQuery.time
		target['Duration'] = targetQuery.duration
	elif reviewDetails['Type'] == "COACHING":
		targetQuery = db.session.query(User.name, User.surname).filter(User.id==reviewDetails['Target']).first()
		target['Name'] = targetQuery.name
		target['Surname'] = targetQuery.surname

	return render_template('client/review.html', segment='review', review=reviewDetails, client=client, target=target)


# Create Workouts Page
@blueprint.route('/workouts')
@login_required
def workouts():
	id = current_user.id
	user = User.query.get_or_404(id)
	# Get all data from workout 
	workouts = db.session.query(WorkoutType.title, Workout.date, Workout.duration, Workout.heart_rate_max, Workout.heart_rate_min, 
				Workout.heart_rate_avg, Workout.calories, Workout.active_calories, Workout.distance, Workout.pace_avg).join(WorkoutType, Workout.workout_type == WorkoutType.id).filter(Workout.client_id==id).order_by(Workout.date.desc())
	return render_template('client/workouts.html', segment='workouts', workouts=workouts)

# Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment
    except: 
        return None
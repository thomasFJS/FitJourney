"""
Author  :        Thomas Fujise
Date    :        11.04.2022
File    :        routes.py
Version :        1.0.0
Brief   :        Set all the application routes
"""

from apps.home import blueprint
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from jinja2 import TemplateNotFound
from dateutil.relativedelta import relativedelta

from flask_login import (
    current_user
)

from apps import db, login_manager
from apps.authentication.models import User, PhysicalInfo, Subscription, Purchase, CoachingReview, SessionReview, Review
from apps.home.forms import UpdateForm

from sqlalchemy import union

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')

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
	q1 = db.session.query(CoachingReview.id, CoachingReview.satisfaction.label("Field1"), CoachingReview.support.label("Field2"), CoachingReview.disponibility.label("Field3"), CoachingReview.is_continuing.label("Field4"))
	q2 = db.session.query(SessionReview.id, SessionReview.difficulty, SessionReview.feel, SessionReview.fatigue, SessionReview.energy)

	#UNION with the 2 queries 
	q3 = union(q1,q2).alias()

	#q4 = aliased(q3, name="If")

	query = db.session.query(Review.id, Review.comment, Review.date, Review.type).select_from(q3).join(Review,Review.id==q3.c.COACHING_REVIEW_id).filter(Review.id_client==id)


	#Set all the reports
	current_user.reports = query

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
		
		try:
			db.session.commit()
			flash("Account Updated successfully !")
			return render_template("home/profile.html",
					form=update_form
			)		
		except:
			flash("Error! Looks like there was a problem.. try again!")
			return render_template("home/profile.html",
					form=update_form
					)
	else:
		return render_template("home/profile.html", segment='profile',
				form=update_form,
				id = id,
				physicalInfo=physicalInfo)

	return render_template("home/profile.html", segment='profile')



# Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment
    except: 
        return None
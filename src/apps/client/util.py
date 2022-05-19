"""
Author  :        Thomas Fujise
Date    :        18.05.2022
File    :        util.py
Version :        1.0.0
Brief   :        All the functions needed to get datas for templates
"""

# APP
from apps.client import blueprint
from apps import db, login_manager
from apps.authentication.models import User, PhysicalInfo, Subscription, Purchase, CoachingReview, WorkoutReview, Review, Workout, WorkoutType, Session, CoachedBy
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

# SQL ALCHEMY 
from sqlalchemy import union, func

# UTILS
from dateutil.relativedelta import relativedelta
import uuid as uuid
import os
import json
from werkzeug.utils import secure_filename

from datetime import date, datetime

def get_next_session(userId):
    """
    Get all the next sessions

    Parameter(s) :
    NAME     |  TYPE  | DESC
    userId   | INT    | The id of the user 


    The query used : 
	 SELECT SESSION.date, SESSION.time, SESSION.duration, WORKOUT_TYPE.title, USER.name, USER.surname
	 FROM SESSION 
	 JOIN WORKOUT_TYPE ON SESSION.workout_type = WORKOUT_TYPE.id 
	 JOIN USER ON USER.id = SESSION.coach_id 
	 WHERE SESSION.client_id = 1 AND SESSION.date > curdate() 
	 ORDER BY SESSION.date
    """
    result = db.session.query(Session.date, Session.time, Session.duration, WorkoutType.title, WorkoutType.logo, User.name, User.surname).join(WorkoutType, Session.workout_type==WorkoutType.id).join(User, Session.coach_id==User.id).filter(Session.client_id==userId).filter(Session.date>date.today()).order_by(Session.date)
    
    return result

def get_review_author(clientId): 
    """
    Get the client who add the review with his id

     Parameter(s):
     NAME     |  TYPE  | DESC
     clientId |  INT   | the id of the client who post the review.
    """
    result = db.session.query(User.name, User.surname).filter(User.id==clientId).first()

    return result


def get_review_details(reviewId, reviewType): 
    """
    Get the details of a review depends on his type

    Parameter(s) :
     NAME      |  TYPE  | DESC
     reviewId  |  INT   | The id of the review
     reviewType| STRING | The type of the review ("WORKOUT" or "COACHING")
    """
    #Queries to get all Review from user 
	#coachingReviewQuery = db.session.query(CoachingReview.id, CoachingReview.satisfaction.label("Field1"), CoachingReview.support.label("Field2"), CoachingReview.disponibility.label("Field3"), CoachingReview.advice.label("Field4"), CoachingReview.target_id.label("target_id"))
	#workoutReviewQuery = db.session.query(WorkoutReview.id, WorkoutReview.difficulty, WorkoutReview.feel, WorkoutReview.fatigue, WorkoutReview.energy, WorkoutReview.target_id)

	#UNION with the 2 queries 
	#reviewsUnion = union(coachingReviewQuery,workoutReviewQuery).alias()

	# Query to get field from Review table and from the review union made before
	#reviewsQuery = db.session.query(Review.id, Review.comment, Review.date, Review.type, reviewsUnion.c.Field1, reviewsUnion.c.Field2, reviewsUnion.c.Field3, reviewsUnion.c.Field4, Review.id_client, reviewsUnion.c.target_id).select_from(reviewsUnion).join(Review,Review.id==reviewsUnion.c.COACHING_REVIEW_id).filter(Review.id_client==id).order_by(Review.date.desc())
    target = {}
    if reviewType == "WORKOUT":
        review = db.session.query(Review.id, Review.comment, Review.date, Review.type, WorkoutReview.difficulty.label("Field1"), WorkoutReview.feel.label("Field2"),
         WorkoutReview.fatigue.label("Field3"), WorkoutReview.energy.label("Field4"),
          Review.id_client, WorkoutReview.target_id).join(Review, Review.id==WorkoutReview.id).filter(Review.id==reviewId).first()
        
        targetQuery = db.session.query(WorkoutType.title, Workout.date, Workout.duration).join(WorkoutType, WorkoutType.id==Workout.workout_type).filter(Workout.id==review.target_id).first()
        
        target['Type'] = targetQuery.title
        target['Date'] = targetQuery.date
        target['Duration'] = targetQuery.duration
    
    elif reviewType == "COACHING":
        review = db.session.query(Review.id, Review.comment, Review.date, Review.type, CoachingReview.satisfaction.label("Field1"), CoachingReview.support.label("Field2"), CoachingReview.disponibility.label("Field3"), CoachingReview.advice.label("Field4"), Review.id_client, CoachingReview.target_id).join(Review, Review.id==CoachingReview.id).filter(Review.id==reviewId).first()
    
        targetQuery = db.session.query(User.name, User.surname).filter(User.id==review.target_id).first()
        target['Name'] = targetQuery.name
        target['Surname'] = targetQuery.surname

    return [review, target]

def get_reviews(clientId):
    """
    Get all the reviews added by user

    Parameter(s):
     NAME     |  TYPE  | DESC
     clientId |  INT   | the id of the client 
    """

    reviews = db.session.query(Review.id, Review.type, Review.date).filter(Review.id_client==clientId).order_by(Review.date.desc())
    
    return reviews

def get_workouts(clientId):
    """
    Get all the workouts done by a client

    Parameter(s) :
     NAME      |  TYPE  | DESC
     clientId  |  INT   | The id of the client
    """
    workouts = db.session.query(WorkoutType.title,Workout.id, Workout.date, Workout.duration, Workout.heart_rate_avg, Workout.calories).join(WorkoutType, Workout.workout_type == WorkoutType.id).filter(Workout.client_id==clientId).order_by(Workout.date.desc())
    
    return workouts        

def get_workout_details(workoutId):
    """
    Get all the details of a workout

    Parameter(s):
    NAME      |  TYPE  | DESC
    workoutId  |  INT   | The id of the workout
    """

    workout =  db.session.query(WorkoutType.title, WorkoutType.logo, Workout.id, Workout.date, Workout.duration, Workout.heart_rate_max, Workout.heart_rate_min, 
				Workout.heart_rate_avg, Workout.calories, Workout.active_calories, Workout.distance, Workout.pace_avg).join(WorkoutType, Workout.workout_type == WorkoutType.id).filter(Workout.id==workoutId).first()

    return workout

def get_workout_review_field():
    """
    Get the fields name for a workout review (the fields names are set in the database)

    Parameter(s):
    /
    """
    fields = db.session.query(WorkoutReview).statement.columns.keys()

    return fields

def is_workout_reviewed(workoutId):
    """
    Check if a workout is already reviewed 

    
    Parameter(s):
    NAME      |  TYPE  | DESC
    workoutId  |  INT   | The id of the workout
    """
    result = db.session.query(WorkoutReview.target_id).filter(WorkoutReview.target_id==workoutId).first() is not None
    return result

def get_user(userId):
    """
    Get user object with id

    Parameter(s):
    NAME      |  TYPE  | DESC
    userId    |  INT   | The id of the user
    """
    user = User.query.filter_by(id=userId).first()

    return user

def get_physical_infos(userId):
    """
    Get the last added physical infos for a user

    Parameter(s):
    NAME      |  TYPE  | DESC
    userId    |  INT   | The id of the user
    """
    infos = PhysicalInfo.query.filter_by(user_id=userId).order_by(PhysicalInfo.date.desc()).first()

    return infos

def get_last_subscription(userId):
    """
    Get the last subsciption purchase date and the duration of the subscription purchased
    
    Parameter(s):
    NAME      |  TYPE  | DESC
    userId    |  INT   | The id of the user
    
    Request in SQL : 
     SELECT `SUBSCRIPTION`.DURATION AS `SUBSCRIPTION_DURATION`, `PURCHASE`.DATE AS `PURCHASE_DATE` 
	 FROM `PURCHASE` 
	 INNER JOIN `SUBSCRIPTION` ON `PURCHASE`.SUBSCRIPTION_ID = `SUBSCRIPTION`.ID 
	 WHERE `PURCHASE`.CLIENT_ID = userId
	 ORDER BY `PURCHASE`.DATE
    
    """
    result = db.session.query(Subscription.duration, Purchase.date).join(Subscription, Purchase.subscription_id==Subscription.id).filter(Purchase.client_id==userId).order_by(Purchase.date).first()

    return result


def get_workout_type_count(clientId):
    """
    Get the count of each type of workout made by user and split workout type count in 2 array (1 for the title and 1 for the count) to use them 
    in javascript with Chart.JS

    Parameter(s) :
     NAME      |  TYPE  | DESC
     clientId  |  INT   | The id of the client

    Return : Array contais 2 differents array. 1 for all the titles and 1 for all the counts
    """
    workoutTypeCount = db.session.query(WorkoutType.title, func.count(Workout.workout_type).label("count")).join(Workout, Workout.workout_type==WorkoutType.id).filter(Workout.client_id==clientId).group_by(Workout.workout_type)
    
    wrktTypeList = []
    wrktTypeCount = []
    print(workoutTypeCount)
    for wtCount in workoutTypeCount:
        wrktTypeList.append('"' +wtCount.title+ '"')
        wrktTypeCount.append(wtCount.count)

    return [wrktTypeList, wrktTypeCount]

def get_workout_count_per_month(clientId):
    """
    Get the number of workout made each month during this year

    Parameter(s) :
     NAME      |  TYPE  | DESC
     clientId  |  INT   | The id of the client

    Return : Array with 12 values represent the 12 months of a year
    """

    count = db.session.query(func.month(Workout.date).label("month"), func.count(Workout.id).label("count")).filter(Workout.client_id==clientId).filter(func.year(date.today())==func.year(Workout.date)).group_by(func.month(Workout.date))
    
    # Create a year array with 12 values (each value represent a month)
    nbWorkoutPerMonth = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(12):
        for wtCountbyMonth in count:
            if i == wtCountbyMonth.month-1: # If month got result from query set the value else keep 0 
                nbWorkoutPerMonth[i] = wtCountbyMonth.count
                break
                    
   
    return nbWorkoutPerMonth
"""
Author  :        Thomas Fujise
Date    :        18.05.2022
File    :        util.py
Version :        1.0.0
Brief   :        All the functions needed to get datas for coach templates
"""

# APP
from apps import db
from apps.authentication.models import User, PhysicalInfo, Subscription, Purchase, CoachingReview, WorkoutReview, Review, Workout, WorkoutType, Session, CoachedBy, Program

# SQL ALCHEMY 
from sqlalchemy import union, func

# UTILS
from dateutil.relativedelta import relativedelta

import json

from datetime import date

from apps.client.util import *

def get_last_workout(userId):
    """
    Get a user last workout done

     Parameter(s):
     NAME     |  TYPE  | DESC
     userId   |  INT   | the id of the user

     Return :
     | Workout() | Workout object only with the properties selected with the query (date) 
    """
    lastWorkout = db.session.query(Workout.date).filter(Workout.client_id==userId).order_by(Workout.date.desc()).first()

    return lastWorkout

def get_coach_next_session(coachId):
    """
    Get the next session of a coach

    Parameter(s):
     NAME     |  TYPE  | DESC
     coachId   |  INT   | the id of the coach

     Return :
     | Query() | Query object with all the properties selected 

     SQL :
        SELECT USER.id, USER.name, USER.surname, USER.card_id, USER.profile_pic SESSION.start_time, SESSION.end_time, SESSION.duration, WORKOUT_TYPE.logo 
        FROM SESSION 
        JOIN USER ON SESSION.client_id = USER.id 
        JOIN WORKOUT_TYPE ON WORKOUT_TYPE.id = SESSION.workout_type 
        WHERE SESSION.start_time >= current_timestamp() 
        ORDER BY SESSION.start_time ASC
    """

    nextSession = db.session.query(User.id, User.name, User.surname, User.card_id, User.profile_pic, Session.start_time, Session.end_time, Session.duration, WorkoutType.logo.label("workoutLogo")).join(User, User.id==Session.client_id).join(WorkoutType, WorkoutType.id==Session.workout_type).filter(Session.coach_id==coachId).filter(Session.start_time>=func.current_timestamp()).order_by(Session.start_time.asc()).first()
    return nextSession



def is_active(userId):
    """
    Check if user was active in the last 24h (by checking if he done a workout)

    Parameter(s):
     NAME     |  TYPE  | DESC
     userId   |  INT   | the id of the user

     Return :
     | Boolean | True if the user done a workout in the last 24h, else False
    """
    isActive = db.session.query(Workout.date).filter(Workout.client_id==userId).filter(Workout.date>=func.current_date()-1).first() is not None

    return isActive

def get_clients(coachId):
    """
    Get all clients coached by a coach
    
    Parameter(s):
     NAME     |  TYPE  | DESC
     coachId   |  INT   | the id of the coach

     Return :
     | Array[Dict] | Array of dict, dict contains all properties from user that we need

    """
    clients = db.session.query(User.id, User.name, User.surname, User.card_id, User.profile_pic).join(CoachedBy, CoachedBy.client_id==User.id).filter(CoachedBy.coach_id==coachId)


    result = []
    
    for client in clients:
        result.append({
            'id': client.id,
            'name' : client.name,
            'surname' : client.surname,
            'card_id' : client.card_id,
            'profile_pic' : str(client.profile_pic),
            'subscriptionEnd' : get_subscription_end_date(client.id),
            'lastWorkout' : get_last_workout(client.id),
            'isActive' : is_active(client.id)
        })


    return result

def get_client_details(clientId):
    """
    Get client details with his id

    Parameter(s):
     NAME     |  TYPE  | DESC
     clientId |  INT   | the id of the client

     Return :
     | Dict | Dict, contains all properties (details) from user that we need
    """

    client = db.session.query(User.id, User.name, User.surname, User.email, User.birthdate, User.profile_pic, User.created_at, User.card_id, User.address, User.city, User.country, User.npa).filter(User.id==clientId).first()
    
    
    return client

def get_all_workout_types():
    """
    Get all types of workouts

    Parameter(s):
    NAME     |  TYPE  | DESC
    /        |  /     |  /

    Return :
    | Array[Query()] | Array of query object with all properties selected
    """

    types = db.session.query(WorkoutType.id, WorkoutType.title).order_by(WorkoutType.title.asc())
    return types


def get_sessions(coachId):
    """
    Get all sessions as event and create array to be used with FullCalendar.io

    Parameter(s):
     NAME     |  TYPE  | DESC
     coachId   |  INT   | the id of the coach

    Return :
    | Array[Obj()] | Array of object contains properties required to be an event with FullCalendar (title, start, end)
    """

    sessions = db.session.query(User.name, User.surname, Session.start_time, Session.end_time).join(User, Session.client_id==User.id).filter(Session.coach_id==coachId)

    result = []

    for session in sessions:
        result.append(
            {
                'title': session.name + " " + session.surname, 
                'start' : session.start_time.strftime("%Y-%m-%dT%H:%M:%S"), 
                'end' : session.end_time.strftime("%Y-%m-%dT%H:%M:%S")
            })

    return result

def get_all_subscriptions():
    """
    Get all types of subscriptions available

    Parameter(s):
     NAME     |  TYPE  | DESC
        /     |   /    | /

    Return :
    | Array[Query()] | Array of query object with all subscription properties selected
    """

    subscription = db.session.query(Subscription.id, Subscription.title, Subscription.cost, Subscription.duration).order_by(Subscription.title.asc())

    return subscription


def get_subscription_id(duration):
    """
    Get the id of a subscription by his duration

    Parameter(s):
     NAME     |  TYPE  | DESC
     duration | STRING | the duration of the subscription

    Return :
    | Query | Array of object contains properties required to be an event with FullCalendar (title, start, end)
    """
    id = db.session.query(Subscription.id).filter(Subscription.duration==duration).first()

    return id


def get_program(clientId):
    """
    Get the actual program of a client

    Parameter(s):
     NAME     |  TYPE  | DESC
     clientId |   INT  | the id of the client

    Return :
    | Query | 
    """
    # Get the latest workout program uploaded for this user (Program type : 1 => Diet | 2 => Workout)
    workoutProgram = db.session.query(Program.id, Program.date, Program.type, Program.pdf, User.name, User.surname).join(User, Program.coach_id==User.id).filter(Program.type==2).filter(Program.client_id==clientId).order_by(Program.date.desc()).first() 
    dietProgram = db.session.query(Program.id, Program.date, Program.type, Program.pdf, User.name, User.surname).join(User, Program.coach_id==User.id).filter(Program.type==1).filter(Program.client_id==clientId).order_by(Program.date.desc()).first() 
    
    result = []

    result.append(workoutProgram)
    result.append(dietProgram)
    
    return result
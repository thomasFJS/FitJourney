"""
Author  :        Thomas Fujise
Date    :        18.05.2022
File    :        util.py
Version :        1.0.0
Brief   :        All the functions needed to get datas for client templates
"""

# APP
from apps import db
from apps.authentication.models import User, PhysicalInfo, Subscription, Purchase, CoachingReview, WorkoutReview, Review, Workout, WorkoutType, Session, CoachedBy

# SQL ALCHEMY 
from sqlalchemy import union, func

# UTILS
from dateutil.relativedelta import relativedelta

from datetime import date

def get_next_session(userId):
    """
    Get all the next sessions

    SQL : 
	 SELECT SESSION.start_time, SESSION.end_time, SESSION.duration, WORKOUT_TYPE.title, USER.name, USER.surname
	 FROM SESSION 
	 JOIN WORKOUT_TYPE ON SESSION.workout_type = WORKOUT_TYPE.id 
	 JOIN USER ON USER.id = SESSION.coach_id 
	 WHERE SESSION.client_id = 1 AND SESSION.start_time > curdate() 
	 ORDER BY SESSION.start_time

    Parameter(s) :
    NAME     |  TYPE  | DESC
    userId   | INT    | The id of the user 

    Return :
    | ARRAY[] | Array with all the next sessions planed for a user
    """
    sessions = db.session.query(Session.start_time, Session.end_time, Session.duration, WorkoutType.title, WorkoutType.logo, User.name, User.surname).join(WorkoutType, Session.workout_type==WorkoutType.id).join(User, Session.coach_id==User.id).filter(Session.client_id==userId).filter(Session.start_time>date.today()).order_by(Session.start_time)

    return sessions

def get_review_author(clientId): 
    """
    Get the client name and surname who add the review with his id

     Parameter(s):
     NAME     |  TYPE  | DESC
     clientId |  INT   | the id of the client who post the review.

     Return :
     | USER() | User name and surname 
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
    
    Return :
    | ARRAY[REVIEW(), ARRAY[]] | Array with the review details and an array that contains the target details of the review
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

    | ARRAY[REVIEW()] | Array with all reviews added by the user
    """

    reviews = db.session.query(Review.id, Review.type, Review.date).filter(Review.id_client==clientId).order_by(Review.date.desc())
    
    return reviews

def get_workouts(clientId):
    """
    Get all the workouts done by a client

    Parameter(s) :
     NAME      |  TYPE  | DESC
     clientId  |  INT   | The id of the client

    Return :
    | ARRAY[WORKOUT()] | Array with all workouts made by user
    """
    workouts = db.session.query(WorkoutType.title,Workout.id, Workout.date, Workout.duration, Workout.heart_rate_avg, Workout.calories).join(WorkoutType, Workout.workout_type == WorkoutType.id).filter(Workout.client_id==clientId).order_by(Workout.date.desc())
    
    return workouts        

def get_workout_details(workoutId):
    """
    Get all the details of a workout

    Parameter(s):
    NAME      |  TYPE  | DESC
    workoutId  |  INT   | The id of the workout

    | OBJECT | Object with all details of the workout as properties
    """

    workout =  db.session.query(WorkoutType.title, WorkoutType.logo, Workout.id, Workout.date, Workout.duration, Workout.heart_rate_max, Workout.heart_rate_min, 
				Workout.heart_rate_avg, Workout.calories, Workout.active_calories, Workout.distance, Workout.pace_avg).join(WorkoutType, Workout.workout_type == WorkoutType.id).filter(Workout.id==workoutId).first()

    return workout

def get_workout_review_field():
    """
    Get the fields name for a workout review (the fields names are set in the database)

    Parameter(s):
    /

    Return :
    | ARRAY[STRING] | Array with the workout review fields name
    """
    fields = db.session.query(WorkoutReview).statement.columns.keys()

    return fields

def get_coaching_review_field():
    """
    Get the fields name for a coaching review (the fields names are set in the database)

    Parameter(s):
    /

    Return :
    | ARRAY[STRING] | Array with the coaching review fields name 
    """
    fields = db.session.query(CoachingReview).statement.columns.keys()
    return fields

def is_workout_reviewed(workoutId):
    """
    Check if a workout is already reviewed 

    
    Parameter(s):
    NAME      |  TYPE  | DESC
    workoutId  |  INT   | The id of the workout

    Return :
    | BOOLEAN | True if the workout is already reviewed, else False
    """
    result = db.session.query(WorkoutReview.target_id).filter(WorkoutReview.target_id==workoutId).first() is not None
    return result

def get_user(userId):
    """
    Get user object with id

    Parameter(s):
    NAME      |  TYPE  | DESC
    userId    |  INT   | The id of the user

    Return :
    | USER() | the user
    """
    user = User.query.filter_by(id=userId).first()

    return user

def get_physical_infos(userId):
    """
    Get the last added physical infos for a user

    Parameter(s):
    NAME      |  TYPE  | DESC
    userId    |  INT   | The id of the user

    Return : 
    | PHYSICALINFO() | the last updated physical infos of the user
    """
    infos = PhysicalInfo.query.filter_by(user_id=userId).order_by(PhysicalInfo.date.desc()).first()

    return infos

def get_subscription_end_date(userId):
    """
    Get the last subsciption purchased end date
    
    Parameter(s):
    NAME      |  TYPE  | DESC
    userId    |  INT   | The id of the user
    
    Request in SQL : 
     SELECT `SUBSCRIPTION`.DURATION AS `SUBSCRIPTION_DURATION`, `PURCHASE`.DATE AS `PURCHASE_DATE` 
	 FROM `PURCHASE` 
	 INNER JOIN `SUBSCRIPTION` ON `PURCHASE`.SUBSCRIPTION_ID = `SUBSCRIPTION`.ID 
	 WHERE `PURCHASE`.CLIENT_ID = userId
	 ORDER BY `PURCHASE`.DATE
    
    Return :
    | DATE | the end date of the last purchased subscription

    """
    subscription = db.session.query(Subscription.duration, Purchase.date).join(Subscription, Purchase.subscription_id==Subscription.id).filter(Purchase.client_id==userId).order_by(Purchase.date.desc()).first()

    #Add duration to the purchase date to get end date
    endDate = (subscription[1] + relativedelta(months=subscription[0]))	
    
    return endDate


def get_workout_type_count(clientId):
    """
    Get the count of each type of workout made by user and split workout type count in 2 array (1 for the title and 1 for the count) to use them 
    in javascript with Chart.JS

    Parameter(s) :
     NAME      |  TYPE  | DESC
     clientId  |  INT   | The id of the client

    Return :
    | ARRAY[ARRAY[STRING], ARRAY[INT]] | Array with 2 differents array inside. 1 for all the titles and 1 for all the counts
    """
    workoutTypeCount = db.session.query(WorkoutType.title, func.count(Workout.workout_type).label("count")).join(Workout, Workout.workout_type==WorkoutType.id).filter(Workout.client_id==clientId).group_by(Workout.workout_type)
    
    wrktTypeList = []
    wrktTypeCount = []

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

    Return : 
    | ARRAY[INT] | Array with 12 int values represent the 12 months of a year. (Each values is the number of workout made for the month)
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

def get_actual_coach_id(clientId):
    """
    Get the actual coach id for a client 

    Parameter(s) :
     NAME      |  TYPE  | DESC
     clientId  |  INT   | The id of the client

    Return :
    | INT | The coach id 
    """

    coachId = db.session.query(CoachedBy.coach_id).filter(CoachedBy.client_id==clientId).order_by(CoachedBy.end_date.desc()).first()

    return coachId

def get_average_calories_last_week(clientId):
    """
    Get the average of calories burned this week

    SQL : 
	 SELECT AVG(calories) FROM WORKOUT WHERE WORKOUT.client_id = clientId AND WEEK(WORKOUT.date) = WEEK(CURDATE()) - 1;

    Parameter(s) :
     NAME      |  TYPE  | DESC
     clientId  |  INT   | The id of the client

    Return :
    | DECIMAL | the average of calories burned rounded to 1 decimal
    """
    calories = db.session.query(func.avg(Workout.calories).label("avg")).filter(Workout.client_id==clientId).filter(func.week(Workout.date)>=func.week(date.today()) -1).first()

    return round(calories.avg,1) if calories.avg != None else 0.0 

def get_average_heart_rate_last_week(clientId):
    """
    Get the average heart rate recorded this week

    SQL :
     SELECT AVG(heart_rate_avg) FROM WORKOUT WHERE WORKOUT.client_id = clientId AND WEEK(WORKOUT.date) = WEEK(CURDATE()) - 1;

    Parameter(s) :
     NAME      |  TYPE  | DESC
     clientId  |  INT   | The id of the client

    Return :
    | DECIMAL | the average of heart rate recorded rounded to 1 decimal
    """
    heart_rate = db.session.query(func.avg(Workout.heart_rate_avg).label("avg")).filter(Workout.client_id==clientId).filter(func.week(Workout.date)>=func.week(date.today()) -1).first()

    return round(heart_rate.avg,1) if heart_rate.avg != None else 0.0

def get_time_working_out_last_week(clientId):
    """
    Get the total time working out recorded this week

    Parameter(s) :
     NAME      |  TYPE  | DESC
     clientId  |  INT   | The id of the client

    Return :
    | DECIMAL | the total time in minute
    """

    subquery = db.session.query((func.extract("hour",Workout.duration)*60*60 + func.extract("minute",Workout.duration)*60+ func.extract("second",Workout.duration)).label("time")).filter(Workout.client_id==clientId).filter(func.week(Workout.date)>func.week(date.today())-1)
    result = 0.0

    for workout in subquery:
        result += workout.time
    

    return result /60
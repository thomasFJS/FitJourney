"""
Author  :        Thomas Fujise
Date    :        11.04.2022
File    :        models.py
Version :        1.0.0
Brief   :        ALl models needed by the application
"""

from flask_login import UserMixin
from datetime import datetime 
from apps import db, login_manager

from apps.authentication.util import hash_pass


class User(db.Model, UserMixin):

    __tablename__ = 'USER'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    birthdate = db.Column(db.Date)
    card_id = db.Column(db.Integer, unique=True)
    profile_pic = db.Column(db.String(250), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    country = db.Column(db.String(64), nullable=True)
    address = db.Column(db.String(64), nullable=True)
    npa = db.Column(db.String(32), nullable=True)
    is_active = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.Integer, db.ForeignKey('ROLE.id'))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must un pack it's value
            # when **kwargs is request.form, some values will be a 1-element list
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value) # set the attribute

    def __repr__(self):
        return str(self.email)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class PhysicalInfo(db.Model):
    __tablename__ = "PHYSICAL_INFO"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'))

    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Numeric(3,1), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bmi = db.Column(db.Numeric(3,1), nullable=False)
    bmr = db.Column(db.Numeric(5,1), nullable=False)
    bodyfat_percentage = db.Column(db.Numeric(3,1), nullable=False)
    muscle_mass_percentage = db.Column(db.Numeric(3,1), nullable=False)
    bone_mass_percentage = db.Column(db.Numeric(3,1), nullable=False)
    water_percentage = db.Column(db.Numeric(3,1), nullable=False)
    protein_percentage = db.Column(db.Numeric(3,1), nullable=False)
    bone_mass = db.Column(db.Numeric(3,1), nullable=False)
    muscle_mass = db.Column(db.Numeric(4,1), nullable=False)
    bodyfat_mass = db.Column(db.Numeric(4,1), nullable=False)
    leanbody_mass = db.Column(db.Numeric(4,1), nullable=False)
    fat_visceral = db.Column(db.Numeric(4,1), nullable=False)
    body_age = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    front_photo = db.Column(db.String(250), nullable=True)
    right_side_photo = db.Column(db.String(250), nullable=True)
    left_side_photo = db.Column(db.String(250), nullable=True)
    back_photo = db.Column(db.String(250), nullable=True)


class Role(db.Model):
    __tablename__ = 'ROLE'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

class Workout(db.Model):
    __tablename__ = 'WORKOUT'

    id = db.Column(db.Integer, primary_key=True)
    workout_type = db.Column(db.Integer, db.ForeignKey('WORKOUT_TYPE.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('USER.id'))
    date = db.Column(db.DateTime)
    duration = db.Column(db.Time)
    heart_rate_max = db.Column(db.Numeric)
    heart_rate_min = db.Column(db.Numeric)
    heart_rate_avg = db.Column(db.Numeric)
    calories = db.Column(db.Numeric)
    active_calories = db.Column(db.Numeric)
    distance = db.Column(db.Numeric, nullable=True)
    pace_avg = db.Column(db.Time, nullable=True)

class WorkoutType(db.Model):
    __tablename__ = 'WORKOUT_TYPE'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    description = db.Column(db.String(250))
    logo = db.Column(db.String(250))

class Program(db.Model):
    __tablename__ = 'PROGRAM'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))
    pdf = db.Column(db.LargeBinary)
    client_id = db.Column(db.Integer, db.ForeignKey('USER.id'))
    coach_id = db.Column(db.Integer, db.ForeignKey('USER.id'))

class Session(db.Model):
    __tablename__ = 'SESSION'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    duration = db.Column(db.Time)
    workout_type = db.Column(db.Integer, db.ForeignKey('WORKOUT_TYPE.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('USER.id'))
    coach_id = db.Column(db.Integer, db.ForeignKey('USER.id'))

class Subscription(db.Model):
    __tablename__ = 'SUBSCRIPTION'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    cost = db.Column(db.Integer)
    duration = db.Column(db.Integer)    
    
class Purchase(db.Model):
    __tablename__ = 'PURCHASE'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('USER.id'))
    date = db.Column(db.DateTime)
    subscription_id = db.Column(db.Integer, db.ForeignKey('SUBSCRIPTION.id'))

class CoachedBy(db.Model):
    __tablename__ = 'COACHEDBY'

    client_id = db.Column(db.Integer, db.ForeignKey('USER.id'), primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('USER.id'), primary_key=True)
    starting_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime, nullable=True)

class CoachingReview(db.Model):
    __tablename__ = 'COACHING_REVIEW'

    id = db.Column(db.Integer, db.ForeignKey('REVIEW.id') , primary_key=True)
    satisfaction = db.Column(db.Integer, nullable=False)
    support = db.Column(db.Integer, nullable=False)
    disponibility = db.Column(db.Integer, nullable=False)
    is_continuing = db.Column(db.Boolean, nullable=False)

class SessionReview(db.Model):
    __tablename__ = 'SESSION_REVIEW'

    id = db.Column(db.Integer, db.ForeignKey('REVIEW.id') ,primary_key=True)
    difficulty = db.Column(db.Integer, nullable=False)
    feel = db.Column(db.Integer, nullable=False)
    fatigue = db.Column(db.Integer, nullable=False)
    energy = db.Column(db.Integer, nullable=False)

class Review(db.Model):
    __tablename__ = 'REVIEW'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(250), nullable=True)
    date = db.Column(db.DateTime)
    type = db.Column(db.String(15), nullable=False)
    id_client = db.Column(db.Integer, db.ForeignKey('USER.id'))

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    return user if user else None


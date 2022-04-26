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


class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    birthdate = db.Column(db.Date)
    cards_id = db.Column(db.Integer, unique=True)
    logo = db.Column(db.String(250), nullable=True)
    address = db.Column(db.String(64), nullable=True)
    npa = db.Column(db.String(32), nullable=True)
    height = db.Column(db.Numeric, nullable=True)
    weight = db.Column(db.Numeric, nullable=True)
    is_active = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))

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


class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

class Workouts(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    workout_type = db.Column(db.Integer, db.ForeignKey('workoutsType.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    date = db.Column(db.DateTime)
    duration = db.Column(db.Time)
    heart_rate_max = db.Column(db.Numeric)
    heart_rate_min = db.Column(db.Numeric)
    heart_rate_avg = db.Column(db.Numeric)
    calories = db.Column(db.Numeric)
    active_calories = db.Column(db.Numeric)
    distance = db.Column(db.Numeric, nullable=True)
    pace_avg = db.Column(db.Time, nullable=True)

class WorkoutsType(db.Model):
    __tablename__ = 'workoutsType'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    description = db.Column(db.String(250))
    logo = db.Column(db.String(250))

class Programs(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))
    pdf = db.Column(db.LargeBinary)
    client_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    coach_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

class Sessions(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    duration = db.Column(db.Time)
    workout_type = db.Column(db.Integer, db.ForeignKey('workoutsType.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    coach_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    cost = db.Column(db.Integer)
    duration = db.Column(db.Integer)    
    
class Purchases(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    date = db.Column(db.DateTime)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'))

class CoachedBy(db.Model):
    __tablename__ = 'coachedBy'

    client_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    starting_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime, nullable=True)

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = Users.query.filter_by(email=email).first()
    return user if user else None


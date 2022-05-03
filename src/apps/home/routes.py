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

from flask_login import (
    current_user
)

from apps import db, login_manager
from apps.authentication.models import User, PhysicalInfo
from apps.home.forms import UpdateForm


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
	physicalInfo = PhysicalInfo.query.filter_by(user_id=id).order_by(PhysicalInfo.date).first()
	current_user.physicalInfo = physicalInfo

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
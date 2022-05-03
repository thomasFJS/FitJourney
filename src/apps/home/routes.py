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
from apps.authentication.models import User
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
	name_to_update = User.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.surname = request.form['surname']
		name_to_update.email = request.form['email']
		name_to_update.birthdate = request.form['birthdate']
		name_to_update.address = request.form['address']
		name_to_update.city = request.form['city']
		name_to_update.country = request.form['country']
		name_to_update.npa = request.form['npa']
		
		try:
			db.session.commit()
			flash("Account Updated successfully !")
			return render_template("home/profile.html",
					form=update_form,
					name_to_update= name_to_update
			)		
		except:
			flash("Error! Looks like there was a problem.. try again!")
			return render_template("home/profile.html",
					form=update_form,
					name_to_update=name_to_update
					)
	else:
		return render_template("home/profile.html", segment='profile',
				form=update_form,
				name_to_update = name_to_update,
				id = id)

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
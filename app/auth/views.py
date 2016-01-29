from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_user, logout_user, login_required, current_user

from .forms import loginForm
from . import auth
from ..models import Catergory, Post, User
from .. import login_manager
from ..main.views import get_catergories


@auth.route('/login', methods=['GET', 'POST'])
def login():
	catergories = get_catergories()
	form = loginForm()
	if form.validate_on_submit():
		username = User.query.filter_by(username=form.username.data).first()
		if username is not None and username.verify_password(form.password.data):
			login_user(username, form.remember_me.data)
			flash("Welcome {}".format(current_user.username))
			return redirect(request.args.get('next') or url_for('main.home'))
		else:
			flash('Wrong username or password. Try again.')
	return render_template('auth/login.html', form=form, catergories=catergories)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logged out')
    return redirect(url_for('main.home'))
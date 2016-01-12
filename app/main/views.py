from flask import render_template, session, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask.ext.login import login_user, logout_user, login_required


from . import main
from .forms import loginForm
from .. import db
from ..models import Catergory, Post, User
from .. import login_manager



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@main.route('/')
@main.route('/page/<int:page>')
def home(page=1):
	posts = Post.query.order_by(Post.pub_date.desc()).paginate(page, 2, False)
	catergories = []

	for catergory in Catergory.query.all():
		post_count = Post.query.filter_by(catergory_id=catergory.id).count()
		catergories.append((catergory, post_count))

	return render_template('home.html', posts=posts, catergories=catergories)



@main.route('/login', methods=['GET', 'POST'])
def login():
	form = loginForm()
	if form.validate_on_submit():
		username = User.query.filter_by(username=form.username.data).first()
		if username is not None and username.verify_password(form.password.data):
			login_user(username, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.home'))
		else:
			flash('Wrong username or password. Try again.')
	return render_template('login.html', form=form)



@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    """
	form = writeForm()
	if form.validate_on_submit():

		title = form.title.data
		article = form.article.data
		db.session.add(Post(title, article))
		db.session.commit()
		return redirect(url_for('home'))
    """
    all_catergories = Catergory.query.all()
    if request.method == 'POST':
    	title = request.form['title']
    	article = request.form['article']
    	# catergory_select = request.form['catergory']
    	catergory_select = request.form['catergory']
    	
    	catergory_search = Catergory.query.filter_by(name=catergory_select).first()
    	if catergory_search:
	    	db.session.add(Post(title=title, article=article, pub_date=datetime.utcnow(), catergory=catergory_search))
        else:
	    	db.session.add(Post(title=title, article=article, pub_date=datetime.utcnow(), catergory=Catergory(name=catergory_select)))
    	db.session.commit()
    	return redirect(url_for('main.home'))

    return render_template('write.html', all_catergories=all_catergories)


@main.route('/addcatergory', methods=['POST'])
@login_required
def add_catergory():
	if request.method == 'POST':
		name = request.form['catergory']
		catergory = Catergory(name=name)
		db.session.add(catergory)
		db.session.commit()
		return redirect(url_for('main.write'))



@main.route('/article/<int:post_id>')
def article(post_id): 
	# same_catergory_post_ids = None
	# post = Post.query.filter_by(id=post_id).first()
	post = Post.query.get(post_id)
	# if post:
		# filter_catergory = Catergory.query.filter_by(name=post.catergory.name).first()
		# some_catergory_posts = filter_catergory.posts
		# print same_catergory_post_ids
	catergories = []
	for catergory in Catergory.query.all():
		post_count = Post.query.filter_by(catergory_id=catergory.id).count()
		catergories.append((catergory, post_count))
	return render_template('article.html', post=post, catergories=catergories)


@main.route('/<catergory_name>')
@main.route('/<catergory_name>/<int:page>')
def articles_of_catergory(catergory_name, page=1):
	catergories = []
	for catergory in Catergory.query.all():
		post_count = Post.query.filter_by(catergory_id=catergory.id).count()
		catergories.append((catergory, post_count))
	catergory= Catergory.query.filter_by(name=catergory_name).first()
	posts= catergory.posts.order_by(Post.pub_date.desc()).paginate(page, 2, False)
	# posts = Post.query.filter_by(catergory.id).paginate(page, 2, False)
	return render_template('catergory.html', posts=posts, catergories=catergories, catergory_name=catergory_name)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logged out')
    return redirect(url_for('main.home'))

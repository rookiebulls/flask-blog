from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager, login_user, logout_user, UserMixin, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HAHAHA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(os.path.abspath(os.path.dirname(__file__)),'posts.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



class Catergory(db.Model):

	__tablename__ = 'catergory'

	id = db.Column(db.Integer, primary_key=True)
	name  = db.Column(db.String(20))
	posts = db.relationship('Post', backref='catergory', lazy='dynamic')

	# def __init__(self, name):
		# self.name = name

	# def __repr__(self):
		# return '<catergory:%r' % self.name



class Post(db.Model):

	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	article = db.Column(db.Text)
	pub_date = db.Column(db.DateTime)
	catergory_id = db.Column(db.Integer, db.ForeignKey('catergory.id'))


	# def __init__(self, title, article):
		# self.title = title
		# self.article = article
		# self.pub_date = datetime.utcnow()

	def __repr__(self):
		return '<tilele:%r' % self.title





class User(UserMixin, db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)


	# def __init__(self, username, password, active=True):
		# self.username = username
		# self.password = self.set_password(password)
		# self.password_hash = generate_password_hash(password)
		# self.active = active		


	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def is_active(self):
		# return self.active
		return True

	def is_authenticated(self):
		return True

	def is_anonymous(self):
		return False

	def __repr__(self):
		return '<user:%r' % self.username		




class loginForm(Form):
	username = StringField('Username', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Login')


class writeForm(Form):
	title = StringField('Title', validators=[Required()])
	article = TextAreaField('Article', validators=[Required()])
	submit = SubmitField('Publish')




@app.route('/')
@app.route('/page/<int:page>')
def home(page=1):
	posts = Post.query.order_by(Post.pub_date.desc()).paginate(page, 2, False)

	catergories = []
	for catergory in Catergory.query.all():
		post_count = Post.query.filter_by(catergory_id=catergory.id).count()
		catergories.append((catergory, post_count))

	return render_template('home.html', posts=posts, catergories=catergories)



@app.route('/login', methods=['GET', 'POST'])
def login():
	form = loginForm()
	if form.validate_on_submit():
		username = User.query.filter_by(username=form.username.data).first()
		if username is not None and username.verify_password(form.password.data):
			login_user(username, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('home'))
		else:
			flash('Wrong username or password. Try again.')
	return render_template('login.html', form=form)



@app.route('/write', methods=['GET', 'POST'])
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
    if request.method == 'POST':
    	title = request.form['title']
    	article = request.form['article']
    	catergory_select = request.form['catergory']
    	catergory_search = Catergory.query.filter_by(name=catergory_select).first()
    	if catergory_search:
	    	db.session.add(Post(title=title, article=article, pub_date=datetime.utcnow(), catergory=catergory_search))
        else:
	    	db.session.add(Post(title=title, article=article, pub_date=datetime.utcnow(), catergory=Catergory(name=catergory_select)))
    	db.session.commit()
    	return redirect(url_for('home'))

    return render_template('write.html')


@app.route('/article/<int:post_id>')
def article(post_id): 
	# same_catergory_post_ids = None
	post = Post.query.filter_by(id=post_id).first()
	# if post:
		# filter_catergory = Catergory.query.filter_by(name=post.catergory.name).first()
		# some_catergory_posts = filter_catergory.posts
		# print same_catergory_post_ids
	catergories = []
	for catergory in Catergory.query.all():
		post_count = Post.query.filter_by(catergory_id=catergory.id).all()
		catergories.append((catergory, len(post_count)))
	return render_template('article.html', post=post, catergories=catergories)


@app.route('/<catergory_name>')
def articles_of_catergory(catergory_name):
	catergories = []
	for catergory in Catergory.query.all():
		post_count = Post.query.filter_by(catergory_id=catergory.id).all()
		catergories.append((catergory, len(post_count)))
	catergory= Catergory.query.filter_by(name=catergory_name).first()
	posts_of_catergory = catergory.posts
	return render_template('catergory.html', posts_of_catergory=posts_of_catergory, catergories=catergories)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True)

from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager, login_user, logout_user, UserMixin, login_required
from werkzeug.security import generate_password_hash, check_password_hash

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



class Post(db.Model):

	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	article = db.Column(db.String, nullable=False)


	def __init__(self, title, article):
		self.title = title
		self.article = article

	def __repr__(self):
		return '<tilele:%r' % self.title


class User(UserMixin, db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)


	def __init__(self, username, password, active=True):
		self.username = username
		# self.password = self.set_password(password)
		self.password_hash = generate_password_hash(password)
		self.active = active		


	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)


	def is_active(self):
		return self.active

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
def home():
	posts = Post.query.all()
	posts = posts[::-1]
	return render_template('home.html', posts=posts)



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
    	db.session.add(Post(title, article))
    	db.session.commit()
    	return redirect(url_for('home'))

    return render_template('write.html')


@app.route('/article/<int:post_id>')
def article(post_id):
	posts = Post.query.filter_by(id=post_id).all()
	return render_template('article.html', posts=posts)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True)

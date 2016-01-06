from flask import Flask, render_template, session, redirect, url_for, flash, g
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HAHAHA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(os.path.abspath(os.path.dirname(__file__)),'posts.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

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


class loginForm(Form):
	username = StringField('username', validators=[Required()])
	password = PasswordField('password', validators=[Required()])
	submit = SubmitField('Submit')


class writeForm(Form):
	title = StringField('title', validators=[Required()])
	article = TextAreaField('article', validators=[Required()])
	submit = SubmitField('Submit')




@app.route('/')
def home():
	posts = Post.query.all()
		# print posts
	return render_template('home.html', posts=posts)



@app.route('/login', methods=['GET', 'POST'])
def login():
	form = loginForm()
	if form.validate_on_submit():
		if form.username.data == 'admin' and form.password.data == 'admin':
			session['logged_in'] = True
			return redirect(url_for('home'))
		else:
			flash('Wrong username or password. Try again.')
	return render_template('login.html', form=form)

@app.route('/write', methods=['GET', 'POST'])
def write():

	form = writeForm()
	if not session.get('logged_in'):
		flash('You need to login first')
		return redirect(url_for('home'))
	if form.validate_on_submit():

		title = form.title.data
		article = form.article.data
		db.session.add(Post(title, article))
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('write.html', form=form)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('you have logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True)

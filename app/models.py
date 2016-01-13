from . import db
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Catergory(db.Model):

	__tablename__ = 'catergory'

	id = db.Column(db.Integer, primary_key=True)
	name  = db.Column(db.String(20))
	posts = db.relationship('Post', backref='catergory', lazy='dynamic')


	def __repr__(self):
		return '<catergory:%r' % self.catergory




class Post(db.Model):

	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	article = db.Column(db.Text)
	pub_date = db.Column(db.DateTime)
	catergory_id = db.Column(db.Integer, db.ForeignKey('catergory.id'))


	def __repr__(self):
		return '<tilele:%r' % self.title





class User(UserMixin, db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)

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



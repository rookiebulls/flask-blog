from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import Required

class loginForm(Form):
	username = StringField('Username', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Login')


class writeForm(Form):
	title = StringField('Title', validators=[Required()])
	article = TextAreaField('Article', validators=[Required()])
	submit = SubmitField('Publish')
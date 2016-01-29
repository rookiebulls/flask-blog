from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required



class writeForm(Form):
	title = StringField('Title', validators=[Required()])
	catergory = SelectField('Catergory',  validators=[Required()])
	content = TextAreaField('Content', validators=[Required()])
	submit = SubmitField('Publish')
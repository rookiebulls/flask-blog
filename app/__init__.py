from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.moment import Moment


from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	db.init_app(app)
	moment.init_app(app)
	login_manager.init_app(app)
	from .main import main 
	app.register_blueprint(main)

	from .auth import auth 
	app.register_blueprint(auth, url_prefix='/auth')

	return app

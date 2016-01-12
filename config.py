import os

basedirf = os.path.abspath(os.path.dirname(__file__))

class Config:
	DEBUG = False
	SECRECT_KEY = os.environ.get('SECRECT_KEY') or 'rookiebulls'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(os.path.abspath(os.path.dirname(__file__)),'posts.db')


class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(os.path.abspath(os.path.dirname(__file__)),'posts.db')


class TestingConfig(Config):
	TESTING = True


config = {
	'developmnet': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': Config
}

	
	
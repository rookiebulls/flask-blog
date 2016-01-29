import os


class Config:
	DEBUG = False
	SECRET_KEY = os.environ.get('SECRECT_KEY') or 'rookiebulls'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	ITEMS_PER_PAGE = 5

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SECRET_KEY = 'development'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(os.path.abspath(os.path.dirname(__file__)),'posts.db')


class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(os.path.abspath(os.path.dirname(__file__)),'posts.db')


class TestingConfig(Config):
	TESTING = True


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': Config
}

	
	
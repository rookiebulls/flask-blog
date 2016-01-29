import os
from app import create_app, db
from app.models import Catergory, Post, User
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash

app = create_app(os.getenv('FLASK_CONFIG') or 'production')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, Post=Post, Catergory=Catergory, User=User)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0", port=os.environ.get('PORT', 5000)))


@manager.command
def test():
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def adduser(username):
	"""Register a user"""
	from getpass import getpass
	password = getpass()
	password2 = getpass('Confirm:')
	if password != password2:
		import sys
		sys.exit("password not mathc")
	db.create_all()
	user = User(username=username, password_hash=generate_password_hash(password))
	db.session.add(user)
	db.session.commit()
	print "User {} has registered successfully.".format(username)



if __name__ == '__main__':
	manager.run()

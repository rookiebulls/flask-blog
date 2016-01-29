from app import db, create_app
from app.models import Post, User, Catergory
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'production')

with app.app_context():

	db.drop_all()
	db.create_all()


	# catergory_one = Catergory(name='Python')
	# catergory_two = Catergory(name='Ruby')
	# post_one = Post(title='Hello', content='Hello World', catergory=catergory_one)
	# post_two = Post(title='Hi', content='Hi There', catergory=catergory_two)
	# post_three = Post(title='What up', content='What up man', catergory=catergory_two)
	# admin = User(username='administator', password_hash=generate_password_hash('ytmdqyuv'))


	# db.session.add(catergory_one)
	# db.session.add(catergory_two)
	# db.session.add(post_one)
	# db.session.add(post_two)
	# db.session.add(post_three)
	# db.session.add(admin)

	# db.session.commit()
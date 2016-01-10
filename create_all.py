from app import db
from app import Post, User, Catergory
from werkzeug.security import generate_password_hash
from datetime import datetime

db.drop_all()
db.create_all()


catergory_one = Catergory(name='Python')
catergory_two = Catergory(name='Ruby')
post_one = Post(title='Hello', article='Hello World', pub_date=datetime.utcnow(), catergory=catergory_one)
post_two = Post(title='Hi', article='Hi There', pub_date=datetime.utcnow(), catergory=catergory_two)
admin = User(username='admin', password_hash=generate_password_hash('admin'))


db.session.add(catergory_one)
db.session.add(catergory_two)
db.session.add(post_one)
db.session.add(post_two)
db.session.add(admin)

db.session.commit()




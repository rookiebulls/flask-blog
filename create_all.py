from app import db
from app import Post, User

db.drop_all()
db.create_all()

first_art = Post('Hello', 'Hello World')
admin = User('admin', 'admin')

db.session.add(first_art)
db.session.add(admin)

db.session.commit()




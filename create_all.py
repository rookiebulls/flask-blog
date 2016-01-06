from app import db
from app import Post

db.create_all()

first_art = Post('Hello', 'Hello World')

db.session.add(first_art)

db.session.commit()




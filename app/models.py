from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

''' models are the underlying logic that goes to the views '''

# Database for all users
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Database for all posts
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # the default argument sets this column to whatever is in that field, here it is datetime.utcnow
    # cont. notice that it is datetime.utcnow not datetime.utcnow(),
    # cont. the former sends the object and sets it for each now post
    # cont. the latter would set every post to the same time, e.g. the time of running the server
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # A ForeignKey links a blog post to the user that authored it
    # cont. the user.id is the unique code for each user
    # cont. thus both db's are tied in a one-to-many fashion, e.g. one user to many posts
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return ('<Post {}>'.format(self.body))


# this is required for flask-login to load users for its authentication
@login.user_loader
def load_user(id):
    # flask-login will pass the load_user function a string and so we must make it an int
    # cont. because our database uses numeric ID's
    return User.query.get(int(id))
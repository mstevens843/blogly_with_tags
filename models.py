"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=False, default="https://cdn-icons-png.flaticon.com/512/149/149071.png")

    # Method to return the full name of the user.
    # We can call this method whenever we need the full name in other files.
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Foreign key for the User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Define relationship to between post model and user model. One to many relationship. 
    # backreg post creates reverse relationship, allowing you to access posts for specific user
    # by calliung user.posts.
    # one user can have many posts, but a post can only have 1 user. 
    user = db.relationship('User', backref='posts')


def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)

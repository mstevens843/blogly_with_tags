"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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

def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)

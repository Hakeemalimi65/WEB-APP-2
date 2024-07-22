from flask_login import UserMixin
from .import db
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),nullable=False)
    email = db.Column(db.String(200),nullable=False,unique=True)
    password = db.Column(db.String(150),nullable=False)
    posts = db.relationship("Post",backref="user")

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
from datetime import datetime
from sqlalchemy import desc, asc,ForeignKey
from sqlalchemy.orm import relationship
from bookmarks import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class Bookmark(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text,nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship('User')

    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)
    def __repr__(self):
        return "<Bookmark {}:{}.".format(self.description, self.url)


class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    bookmarks = db.relationship('Bookmark', backref='user',lazy='select')
    password_hash = db.Column(db.String(300))
    
    def __repr__(self):
        return "<User {}>".format(self.username)
    
    @property
    def password(self):
        raise AttributeError('password: write only-field')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

actors_movies = db.Table('actor_movies',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
     db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
     )

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(225))
    release_date = db.Column(db.DateTime, default=datetime.utcnow)
    actors = db.relationship('Actor', secondary=actors_movies, backref='movie', lazy='select')


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

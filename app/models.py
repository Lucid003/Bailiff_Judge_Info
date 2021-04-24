from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin # includes generic implementations for most user model classes
from werkzeug.security import generate_password_hash, check_password_hash
from jose import jwt
from app import db, login  # these are imported from the __init__.py file

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)
  permissions = db.Column(db.Integer) # 0=user, 1=Manager, 2=Admin
  judge = db.Column(db.String(64))
  

  def __repr__(self):
    return '<User {}>'.format(self.username)
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def get_reset_password_token(self, expires_in=600):
    return jwt.encode(
      {'reset_password': self.id, 'exp': time() + expires_in},
      current_app.config['SECRET_KEY'],
      algorithm='HS256')
  
  @staticmethod
  def verify_reset_password_token(token):
    try:
      id = jwt.decode(token, current_app.config['SECRET_KEY'],
                      algorithms=['HS256'])['reset_password']
    except:
      return
    return User.query.get(id)


@login.user_loader
def load_user(id):
  return User.query.get(int(id))


class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50))
  body = db.Column(db.String(10000))
  judge_id = db.Column(db.Integer, db.ForeignKey('judge.id'))

  def __repr__(self):
    return '<Post {}>'.format(self.body)


class Judge(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))
  posts = db.relationship('Post', backref='judge', lazy='dynamic')
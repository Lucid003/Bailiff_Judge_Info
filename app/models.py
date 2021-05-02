import datetime
from dateutil.relativedelta import relativedelta, MO, FR
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
  displayname = db.Column(db.String(64), unique=True)
  password_hash = db.Column(db.String(128))
  about_me = db.Column(db.String(500))
  last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)
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
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
  judge_id = db.Column(db.Integer, db.ForeignKey('judge.id'))

  def __repr__(self):
    return '<Post {}>'.format(self.body)


class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  content = db.relationship('Post', backref='category', lazy='dynamic')


class Judge(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))
  posts = db.relationship('Post', backref='judge', lazy='dynamic')

  def avatar(self):
    return 'https://bailiffjudgeinfo.stingchameleon.repl.co/static/{}.jpg'\
            .format(self.name)

class Workday(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  weekday = db.Column(db.String(9))
  date = db.Column(db.Date)
  data = db.Column(db.Text)

# helper function to find last monday
def last_monday():
  today = datetime.date.today()
  last_monday = today + relativedelta(weekday=MO(-1))
  return last_monday

# helper function to find next week's friday
# used for preset 2-week schedule
def next_week_friday():
  end = last_monday() + relativedelta(weeks=+1, weekday=FR(+1))
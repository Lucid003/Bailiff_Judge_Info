from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
  jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import PostForm
from app.models import User, Judge, Post
from app.main import bp

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required  # protects index from not-logged-in users
def index():
  judges = Judge.query.all()
  return render_template("index.html", judges=judges)
  

@bp.route('/judge/<judgename>', methods=['GET', 'POST'])
@login_required
def judge(judgename):
  judge = Judge.query.filter_by(name=judgename).first_or_404()
  # categories = judge.
  form = PostForm()
  posts = Post.query.join(Judge.posts)
  return render_template('judge.html', judge=judge, 
                         posts=posts, form=form)
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
  jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import PostForm, EditPostForm
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
  if form.validate_on_submit():
    post = Post(body=form.post.data, title=form.title.data, judge_id=judge.id)
    db.session.add(post)
    db.session.commit()
    flash('Your post is now live!')
    return redirect(url_for('main.judge', judgename=judgename))
  posts = judge.posts.filter(Judge.id==Post.id)

  if posts.count() > 0:
    return render_template('judge.html', judge=judge, 
                           posts=posts, form=form)
  else:
    return render_template('judge.html', judge=judge, 
                           form=form)


@bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
  judgename = request.args.get('judgename')
  post = db.session.query(Post).filter(Post.id==id).first()
  form = EditPostForm(post.title, post.body)
  if form.validate_on_submit():
    if form.delete.data == 1:
      db.session.delete(post)
    else:
      post.title = form.title.data
      post.body = form.post.data
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('main.judge', judgename=judgename))
  elif request.method == "GET":
    form.title.data = post.title
    form.post.data = post.body
  return render_template('edit_post.html', judgename=judgename,
                         form=form)
  

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm(current_user.username)
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash(_('Your changes have been saved.'))
    return redirect(url_for('main.edit_profile'))
  elif request.method == "GET":
    form.username.data = current_user.username # pre-populated the form with the data already stored in database
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title=_('Edit Profile'), 
                         form=form)
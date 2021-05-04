import os
import imghdr
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
  jsonify, current_app, abort
from flask_login import current_user, login_required
from app import db
from app.main.forms import PostForm, EditPostForm, EditProfileForm, UploadForm
from app.models import User, Judge, Post, Category
from app.main import bp
from werkzeug.utils import secure_filename
from app.schedule.import_sched import import_schedule
from xlrd import inspect_format



@bp.before_request # decorator from Flask registers the function to be executed before the view function
def before_request():
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()


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
  categories = Category.query.all()
  form = PostForm()
  form.category.choices = [(cat.id, cat.name) for cat in categories]
  if form.validate_on_submit():
    cat_id = Category.query.filter_by(name=form.category.data)
    post = Post(body=form.post.data,
                judge_id=judge.id,
                category_id=form.category.data)
    db.session.add(post)
    db.session.commit()
    flash('Your post is now live!')
    return redirect(url_for('main.judge', judgename=judgename))
  posts = judge.posts.filter(Judge.id==Post.id)\
                            .order_by(Post.category_id.asc())
  if posts.count() > 0:
    cats = {post.category_id for post in posts}
    return render_template('judge.html', judge=judge, 
                           posts=posts, categories=categories,
                           cats=cats, form=form)
  else:
    return render_template('judge.html', judge=judge, 
                           categories=categories, form=form)


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
      post.body = form.post.data
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('main.judge', judgename=judgename))
  elif request.method == "GET":
    form.post.data = post.body
  return render_template('edit_post.html', judgename=judgename,
                         form=form)


@bp.route('/user/<username>') # <username> is a dynamic component
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('user.html', user=user,
                        title="{}'s User Page".format(
                                  current_user.displayname))


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm()
  if form.validate_on_submit():
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('main.user', 
                            username=current_user.username,
                            title="{}'s User Page".format(
                                  current_user.displayname)))
  elif request.method == "GET":
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title='Edit Profile', 
                         form=form)


def validate_image(stream):
  header = stream.read(512)
  stream.seek(0)
  format = imghdr.what(None, header)
  if not format:
    return None
  return '.' + (format if format != 'jpeg' else 'jpg')


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
  if request.method == 'POST':
    upload_file = request.files['file']
    filename = secure_filename(upload_file.filename)
    if filename != '':
      file_ext = os.path.splitext(filename)[1]
      if file_ext in current_app.config['UPLOAD_EXTENSIONS']['excel'] :
        import_schedule(upload_file.read())
      elif file_ext in current_app.config['UPLOAD_EXTENSIONS']['images'] or \
          file_ext == validate_image(upload_file.stream):
        upload_file.save(os.path.join('static/avatars', current_user.get_id()))
      else:
        abort(400)
    return redirect(url_for('main.index'))
  return render_template('upload.html')
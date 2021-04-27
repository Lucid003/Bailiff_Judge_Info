from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm, RegistrationForm, \
                           EditUserForm, ChangePasswordForm
from app.models import User, Judge


@bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data.lower()).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('auth.login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('main.index')
    return redirect(next_page)
  return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
  if current_user.permissions == 2:
    judge_names = [judge.name for judge in Judge.query.all()]
    judge_names.insert(0, 'None')
    permissions = [(0, 'bailiff'), (1, 'manager'), (2, 'admin')]
    form = RegistrationForm()
    form.judge.choices = judge_names
    form.permissions.choices = permissions
    if form.validate_on_submit():
      user = User(username=form.username.data.lower(),
                  displayname=form.displayname.data,
                  judge=form.judge.data,
                  permissions=form.permissions.data)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      flash('{} is now a registered user.'.format(form.username.data))
      return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = ResetPasswordRequestForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      send_password_reset_email(user)
    flash('Check your email for the instructions to reset your password')
    return redirect(url_for('auth.login'))
  return render_template('auth/reset_password_request.html',
                         title='Reset Password', form=form)
  

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  user = User.verify_reset_password_token(token)
  if not user:
    return redirect(url_for('main.index'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    user.set_password(form.password.data)
    db.session.commit()
    flash('Your password has been reset.')
    return redirect(url_for('auth.login'))
  return render_template('auth/reset_password.html', form=form)


@bp.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
  if current_user.permissions == 2:
    judge_names = [judge.name for judge in Judge.query.all()]
    judge_names.insert(0, 'None')
    users = User.query.all()
    user_names = [user.username for user in users]
    permissions = [(0, 'bailiff'), (1, 'manager'), (2, 'admin')]
    form = EditUserForm()
    form.username.choices = user_names
    form.judge.choices = judge_names
    form.permissions.choices = permissions
    if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      if form.delete.data == 1:
        db.session.delete(user)
      else:
        user.displayname = form.displayname.data
        user.judge = form.judge.data
        user.permissions = form.permissions.data
      db.session.commit()
      flash('Your changes have been saved.')
      return redirect(url_for('auth.edit_user'))
    return render_template('auth/edit_user.html', title='Edit User', 
                          form=form)


@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
  form = ChangePasswordForm()
  if form.validate_on_submit():
    if current_user.check_password(form.old_password.data):
      current_user.set_password(form.new_password.data)
      db.session.commit()
      flash('Your password has been changed.')
      return redirect(url_for('main.user', username=current_user.username))
    else:
      flash('Current password incorrect.')
      return redirect(url_for('auth.change_password'))
  return render_template('auth/change_password.html', form=form)
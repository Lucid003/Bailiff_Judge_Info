from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password')# validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(),
                                      EqualTo('password')])
  judge = SelectField('Judge')
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Username already taken.')


class EditUserForm(FlaskForm):
  username = SelectField('Username')
  judge = SelectField('Judge')
  submit = SubmitField('Submit')



class ResetPasswordRequestForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(),
                                               EqualTo('password')])
  submit = SubmitField('Request Password Reset')

class AddUser(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', 
                        validators=[DataRequired(), EqualTo('password')])
  #judge = SelectField('Assigned to Judge', choices) # figure this out
  submit = SubmitField('Add User')
  

class AdminAddUser(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', 
                        validators=[DataRequired(), EqualTo('password')])
  #judge = SelectField('Assigned to Judge', choices) # figure this out
  permissions = SelectField('Permissions', [0, 1, 2])
  submit = SubmitField('Add User')
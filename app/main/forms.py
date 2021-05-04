from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User


class PostForm(FlaskForm):
  category = SelectField('Category', validators=[DataRequired()])
  post = TextAreaField('Add Details Here', validators=[DataRequired()])
  submit = SubmitField('Submit')


class EditPostForm(FlaskForm):
  post = TextAreaField('Add Details Here', validators=[DataRequired()])
  delete = BooleanField('Delete Post?')
  submit = SubmitField('Submit Changes')

  def __init__(self, original_title, original_post, *args, **kwargs):
    super(EditPostForm, self).__init__(*args, **kwargs)
    self.original_title = original_title
    self.original_post = original_post


class EditProfileForm(FlaskForm):
  about_me = TextAreaField('About me',
                           validators=[Length(min=0, max=240)])
  submit = SubmitField('Submit')


class UploadForm(FlaskForm):
  file = FileField('File')
  submit = SubmitField('Submit')
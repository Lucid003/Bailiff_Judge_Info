from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User


class PostForm(FlaskForm):
  title = StringField('Subject', validators=[DataRequired()])
  post = TextAreaField('Say something', validators=[DataRequired()])
  submit = SubmitField('Submit')


class TaskSelection(FlaskForm):
  user_judge = SubmitField("Edit/View My Judge's Details")
  other_judges = SubmitField("View Other Judges' details")

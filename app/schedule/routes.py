from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
  jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import last_monday, next_week_friday, Workday
from app.schedule import bp

@login_required
@bp.route('/schedule', methods=['GET', 'POST'])
def schedule(start_date=last_monday(), end_date=next_week_friday()):
  dates = Workday.query.filter(Workday.date.between(start_date, end_date))
  return render_template('schedule/schedule.html', dates=dates)
  #date_range = end_date - start_date # build calendar range
  #date_list = [start_date + datetime.timedelta(days=x) \
 

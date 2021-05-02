from app import create_app, db
from app.models import User, Post, Judge, Category, Workday
from app.schedule.import_sched import import_schedule

app = create_app()


@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post, 'Judge': Judge,\
    'Category': Category, 'Workday': Workday, \
    'import_schedule': import_schedule}


if __name__ == '__main__':
	app.run(host='0.0.0.0',
	        debug=True)  # add ", debug=True" after host for debug mode

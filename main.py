from app import create_app, db
from app.models import User, Post, Judge

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Judge': Judge}

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True) # add ", debug=True" after host for debug mode
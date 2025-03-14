from app import db
from app.models import User, Judge, Category

judges = ['Grant Forsberg', 'Stephanie Hansen', 'Thomas Harmon', 'Marcena Hendrix', 'John Huber', 'Marcela Keim', 'Sheryl Lohaus', 'Darryl Lowe', 'Jeff Marcuzzo', 'Craig McDermott', 'Stephanie Shearer', 'Derek Vaughn']

for judge in judges:
  j = Judge(name=judge)
  db.session.add(j)
  db.session.commit()

u = User(username='christopher.mccoy', displayname='Christopher', about_me='Bailiff and creator of this site', permissions=2, judge='Marcela Keim')
u.set_password('password')
db.session.add(u)
db.session.commit()


categories = ['Criminal Traffic', 'Arraignments', 'Trials', 'Jail', 'Probate', 'Civil Motions', 'Civil Call', 'Small Claims', 'Judge',' General']
for cat in categories:
  c = Category(name=cat)
  db.session.add(c)
  db.session.commit()

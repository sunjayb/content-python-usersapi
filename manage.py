import sys
from flask.cli import FlaskGroup
from src import create_app, db
from src.api.models import User

# create flask app
app = create_app()
cli = FlaskGroup(create_app=create_app)

# reload database
@cli.command('refresh_db')
def refresh_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

# populate database
@cli.command('pop_db')
def pop_db():
    db.session.add(User(username='scully', email="dscully@example.com", fullname="Dana Scully"))
    db.session.add(User(username='mulder', email="fmulder@example.com", fullname="Fox Mulder"))
    db.session.add(User(username='wskinner', email="wskinner@example.com", fullname="Walter Skinner"))
    db.session.commit()

if __name__ == '__main__':
    cli()

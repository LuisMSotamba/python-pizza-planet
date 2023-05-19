import pytest
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app import flask_app
from app.plugins import db
# flake8: noqa
from app.repositories.models import *
from app.commands.seed_database import seed_data

manager = FlaskGroup(flask_app)

migrate = Migrate()
migrate.init_app(flask_app, db)


@manager.command('test', with_appcontext=False)
def test():
    return pytest.main(['-v', './app/test'])

@manager.command('seed', with_appcontext=True)
def seed(orders=100, customers=15):
    return seed_data(orders, customers)

if __name__ == '__main__':
    manager()

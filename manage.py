import pytest
import click

from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app import flask_app
from app.plugins import db
# flake8: noqa
from app.repositories.models import *
from app.commands.seed_database import seed_data
from app.commands.clean_database import clear_db

manager = FlaskGroup(flask_app)

migrate = Migrate()
migrate.init_app(flask_app, db)


@manager.command('test', with_appcontext=False)
def test():
    return pytest.main(['-v', './app/test','--cov','./app/test'])

@manager.command('seed', with_appcontext=True)
@click.option('--orders', '-o', default=100, help='Orders to be created')
@click.option('--customers', '-c', default=10, help='Customers to be created')
def seed(orders=100, customers=15):
    return seed_data(orders, customers)

@manager.command('clean', with_appcontext=True)
def clean_database():
    clear_db()

if __name__ == '__main__':
    manager()

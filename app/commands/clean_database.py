from app.plugins import db
from app.repositories.models import *

def clear_db():
    if input("WARNING: This will delete all data from the database. Are you sure? (y/n): ").lower() == 'y':
        db.session.query(OrderBeverage).delete()
        db.session.query(OrderDetail).delete()
        db.session.query(Order).delete()
        db.session.query(Ingredient).delete()
        db.session.query(Size).delete()
        db.session.query(Beverage).delete()
        db.session.commit()
        print("Database cleared")
    else:
        print("Aborted")
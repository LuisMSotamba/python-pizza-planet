import datetime
from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker

from app.plugins import db
from app.repositories.models import *
import random

fake = Faker()

from faker.providers import BaseProvider

class PizzaProvider(BaseProvider):

    def ingredients(self):
        return [
            "Pepperoni",
            "Mushrooms",
            "Mozzarella cheese",
            "Tomato sauce",
            "Bell peppers",
            "Onions",
            "Black olives",
            "Italian sausage",
            "Fresh basil",
            "Garlic"
        ]

    def sizes(self):
        return ["Small", "Medium", "Large", "Extra Large", "Party"]
    
    def beverages(self):
        return ["Coffee", "Tea", "Coke", "Sprite"]
    
    def customer(self):
        return {
            'name' : fake.name(),
            'dni' : fake.ssn(),
            'address' : fake.address(),
            'phone' : fake.phone_number()
        }

fake.add_provider(PizzaProvider)

def seed_data(num_orders, num_customers):
    ingredients = fake.ingredients()
    sizes = fake.sizes()
    # Create Ingredients
    try:
        for ingredient in ingredients:
            price = round(random.uniform(0, 5), 2)
            db.session.add(Ingredient(name=ingredient, price=price))
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error creating ingredients: {str(e)}")

    # Create Sizes
    try:
        for size in sizes:
            price = round(random.uniform(0, 5), 2)
            db.session.add(Size(name=size, price=price))
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error creating sizes: {str(e)}")

    # Create Beverages
    try:
        for beverage in fake.beverages():
            price = round(random.uniform(0, 5), 2)
            db.session.add(Beverage(name=beverage, price=price))
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error creating beverages: {str(e)}")

    # Get all the created ingredients, sizes and beverages
    ingredients = Ingredient.query.all()
    sizes = Size.query.all()
    beverages = Beverage.query.all()
    customers = [fake.customer() for i in range(num_customers)]

    # Create Customers and Orders for multiple months
    for _ in range(num_orders):
        random_date = fake.date_between()
        customer = customers[randint(0, len(customers)-1)]

        size = sizes[randint(0, len(sizes) - 1)]
        order = Order(client_name=customer['name'], client_dni=customer['dni'], client_address=customer['address'],
                        client_phone=customer['phone'], date=random_date,
                        total_price=0, size_id=size._id)
        # Add Order Detail
        ingredient_count = randint(0, len(ingredients))
        ingredients_aux = ingredients[:]
        for l in range(ingredient_count):
            ingredient = ingredients_aux[randint(0, len(ingredients_aux) - 1)]
            order_detail = OrderDetail(ingredient_price=ingredient.price, order_id=order._id, ingredient_id=ingredient._id)
            order.detail.append(order_detail)
            ingredients_aux.remove(ingredient)
            order.total_price += ingredient.price

        # Add Order Beverage
        beverages_count = randint(0, len(beverages))
        beverages_aux = beverages[:]
        for l in range(beverages_count):
            beverage = beverages_aux[randint(0, len(beverages_aux) - 1)]
            order_beverage = OrderBeverage(order_id=order._id, beverage_id=beverage._id)
            order.beverage_detail.append(order_beverage)
            beverages_aux.remove(beverage)
            order.total_price += beverage.price

        db.session.add(order)
    db.session.commit()
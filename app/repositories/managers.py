from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column, func, desc
from sqlalchemy import extract

from .models import Ingredient, Order, OrderDetail, Size, Beverage, OrderBeverage, db
from .serializers import (IngredientSerializer, OrderSerializer,
                          SizeSerializer, BeverageSerializer, ReportSerializer ,ma)

import calendar

class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all((OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, ingredient_price=ingredient.price)
                             for ingredient in ingredients))
        cls.session.add_all((OrderBeverage(order_id=new_order._id, beverage_id=beverage._id)
                             for beverage in beverages))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
    

class ReportManager(BaseManager):
    serializer = ReportSerializer

    @classmethod
    def _get_most_requested_ingredient(cls):
        most_requested_ingredient_query = cls.session.query(Ingredient, func.count(OrderDetail.ingredient_id).label('ingredient_count')) \
            .join(OrderDetail.ingredient)\
            .group_by(Ingredient) \
            .order_by(desc('ingredient_count')) \
            .all()
        report = [{'ingredient': most_requested_ingredient[0], 'ingredient_count': most_requested_ingredient[1]} 
                  for most_requested_ingredient in most_requested_ingredient_query ]
        return report
    

    @classmethod
    def _get_months_more_revenue(cls):
        months_more_revenues = cls.session.query(extract('month',Order.date).label('month'), func.sum(Order.total_price).label('revenue')) \
            .group_by(extract('month',Order.date)) \
            .order_by('month') \
            .all()
        report = [{'month':calendar.month_name[month_revenue[0]], 'revenue':month_revenue[1]} for month_revenue in months_more_revenues]
        return report
    

    @classmethod
    def _get_top_customers(cls, top=3):
        best_customers = cls.session.query(Order.client_dni, Order.client_name, func.sum(Order.total_price).label('total_money'))\
            .group_by(Order.client_dni)\
            .order_by(desc('total_money'))\
            .limit(top)
        report = [{'customer_dni': best_register[0], 'customer_name': best_register[1], 'total_money': best_register[2]} 
                  for best_register in best_customers]
        return report


    @classmethod
    def get_statistics(cls):
        report = {}
        report['ingredient_report'] = cls._get_most_requested_ingredient()
        report['order_report'] = cls._get_months_more_revenue()
        report['customer_report'] = cls._get_top_customers()
        return cls.serializer().dump(report)

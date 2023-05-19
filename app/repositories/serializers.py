from app.plugins import ma
from .models import Ingredient, Size, Order, OrderDetail, Beverage, OrderBeverage


class IngredientSerializer(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Ingredient
        load_instance = True
        fields = ('_id', 'name', 'price')


class SizeSerializer(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Size
        load_instance = True
        fields = ('_id', 'name', 'price')


class OrderDetailSerializer(ma.SQLAlchemyAutoSchema):

    ingredient = ma.Nested(IngredientSerializer)

    class Meta:
        model = OrderDetail
        load_instance = True
        fields = (
            'ingredient_price',
            'ingredient'
        )

class BeverageSerializer(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Beverage
        load_instance = True
        fields = (
            '_id', 
            'name', 
            'price'
        )


class OrderBeverageSerializer(ma.SQLAlchemyAutoSchema):
    beverage = ma.Nested(BeverageSerializer)

    class Meta:
        model = OrderBeverage
        load_instance = True
        fields = (
            '_id',
            'beverage'
        )
        
class OrderSerializer(ma.SQLAlchemyAutoSchema):
    size = ma.Nested(SizeSerializer)
    detail = ma.Nested(OrderDetailSerializer, many=True)
    beverage_detail = ma.Nested(OrderBeverageSerializer, many=True)

    class Meta:
        model = Order
        load_instance = True
        fields = (
            '_id',
            'client_name',
            'client_dni',
            'client_address',
            'client_phone',
            'date',
            'total_price',
            'size',
            'detail',
            'beverage_detail'
        )


class IngredientReportSerializer(ma.SQLAlchemyAutoSchema):

    ingredient = ma.Nested(IngredientSerializer)
    ingredient_count = ma.Float()

    class Meta:
        fields = (
            'ingredient',
            'ingredient_count'
        )

class ReportSerializer(ma.SQLAlchemyAutoSchema):

    ingredient_report = ma.Nested(IngredientReportSerializer, many=True)

    class Meta:
        fields = (
            'ingredient_report',
        )
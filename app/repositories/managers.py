from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column

from .models import Ingredient, Order, OrderDetail, Size, db, Beverage, BeverageDetail
from .serializers import (IngredientSerializer, OrderSerializer,
                          SizeSerializer, ma, BeverageSerializer)
from .utils.functions import get_month_name


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

    @classmethod
    def drop_table(cls):
        cls.session.query(cls.model).delete()
        cls.session.commit()


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

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
        cls.session.add_all(
            (OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, ingredient_price=ingredient.price)
             for ingredient in ingredients))
        cls.session.add_all(
            (BeverageDetail(order_id=new_order._id, beverage_id=beverage._id, beverage_price=beverage.price)
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


class ReportManager(BaseManager):

    @classmethod
    def get_orders_by_month(cls):
        orders_by_month = cls.session.query(db.func.extract('month', Order.date).label('month'),
                                            db.func.sum(Order.total_price).label('total')).group_by(
            db.func.extract('month', Order.date)).all(
        )
        orders = []
        for order in orders_by_month:
            orders.append({'month': get_month_name(order.month), 'total': round(order.total, 2), 'index': order.month})
        return orders

    @classmethod
    def get_most_requested_ingredient(cls):
        most_requested_ingredient_sum = cls.session.query(Ingredient.name,
                                                          db.func.sum(OrderDetail.ingredient_price).label(
                                                              'total')).join(OrderDetail).group_by(
            Ingredient.name).order_by(db.func.sum(OrderDetail.ingredient_price).desc()).first()
        most_requested_ingredient_count = cls.session.query(Ingredient.name,
                                                            db.func.count(OrderDetail.ingredient_id).label(
                                                                'total')).join(OrderDetail).group_by(
            Ingredient.name).order_by(db.func.count(OrderDetail.ingredient_id).desc()).first()
        most_requested_ingredient = {
            'most_requested_ingredient_sum': {'name': most_requested_ingredient_sum.name,
                                              'total': round(most_requested_ingredient_sum.total, 2)},
            'most_requested_ingredient_count': {'name': most_requested_ingredient_count.name,
                                                'total': most_requested_ingredient_count.total}
        }
        return most_requested_ingredient

    @classmethod
    def get_best_customers(cls):
        best_client_count = cls.session.query(Order.client_name,
                                              db.func.count(Order.client_name).label('total')).group_by(
            Order.client_name).order_by(db.func.count(Order.client_name).desc()).limit(3)
        best_client_sum = cls.session.query(Order.client_name, db.func.sum(Order.total_price).label('total')).group_by(
            Order.client_name).order_by(db.func.sum(Order.total_price).desc()).limit(3)
        best_customers = {
            'best_client_count': [{'name': client.client_name, 'total': client.total} for client in best_client_count],
            'best_client_sum': [{'name': client.client_name, 'total': round(client.total, 2)} for client in
                                best_client_sum]}

        return best_customers

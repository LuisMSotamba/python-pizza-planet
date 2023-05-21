from app.common.http_methods import GET, POST
from flask import Blueprint, jsonify, request

from ..controllers import OrderController
from app.common.decorators import generic_response

order = Blueprint('order', __name__)


@order.route('/', methods=POST)
@generic_response(POST, success_status_code=201)
def create_order():
    order, error = OrderController.create(request.json)
    return order, error


@order.route('/id/<_id>', methods=GET)
@generic_response(GET)
def get_order_by_id(_id: int):
    order, error = OrderController.get_by_id(_id)
    return order, error


@order.route('/', methods=GET)
@generic_response(GET)
def get_orders():
    orders, error = OrderController.get_all()
    return orders, error

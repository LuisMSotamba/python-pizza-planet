from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..controllers import BeverageController
from app.common.decorators import generic_response

beverage = Blueprint('beverage', __name__)

@beverage.route('/', methods=POST)
@generic_response(POST, success_status_code=201)
def create_beverage():
    beverage, error = BeverageController.create(request.json)
    return beverage, error

@beverage.route('/', methods=GET)
@generic_response(GET)
def get_beverages():
    beverages, error = BeverageController.get_all()
    return beverages, error
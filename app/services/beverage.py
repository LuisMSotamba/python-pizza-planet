from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..controllers import BeverageController

beverage = Blueprint('beverage', __name__)

@beverage.route('/', methods=POST)
def create_beverage():
    beverage, error = BeverageController.create(request.json)
    response = beverage if not error else {'error': error}
    status_code = 201 if not error else 400
    return jsonify(response), status_code
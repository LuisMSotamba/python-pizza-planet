from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import SizeController
from app.common.decorators import generic_response

size = Blueprint('size', __name__)


@size.route('/', methods=POST)
@generic_response(POST, success_status_code=201)
def create_size():
    size, error = SizeController.create(request.json)
    return size, error


@size.route('/', methods=PUT)
@generic_response(PUT)
def update_size():
    size, error = SizeController.update(request.json)
    return size, error


@size.route('/id/<_id>', methods=GET)
@generic_response(GET)
def get_size_by_id(_id: int):
    size, error = SizeController.get_by_id(_id)
    return size, error

@size.route('/', methods=GET)
@generic_response(GET)
def get_all_size():
    size, error = SizeController.get_all()
    return size, error

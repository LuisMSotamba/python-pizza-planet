from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..controllers import IngredientController
from app.common.decorators import generic_response

ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=POST)
@generic_response(POST, success_status_code=201)
def create_ingredient():
    ingredient, error = IngredientController.create(request.json)
    return ingredient, error


@ingredient.route('/', methods=PUT)
@generic_response(PUT)
def update_ingredient():
    ingredient, error = IngredientController.update(request.json)
    return ingredient, error


@ingredient.route('/id/<_id>', methods=GET)
@generic_response(GET)
def get_ingredient_by_id(_id: int):
    ingredient, error = IngredientController.get_by_id(_id)
    return ingredient, error


@ingredient.route('/', methods=GET)
@generic_response(GET)
def get_ingredients():
    ingredients, error = IngredientController.get_all()
    return ingredients, error

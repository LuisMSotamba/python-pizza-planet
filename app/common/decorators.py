from app.common.http_methods import ( GET, POST, PUT )
from flask import jsonify
from functools import wraps

methods = [GET, POST, PUT]

def generic_response(
        method,
        success_status_code: int = 200, 
        error_status_code: int = 400
        ):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if (not method) or not(method in methods):
                raise f"Method {method} does not exist"
            instance, error = func(*args, **kwargs)
            response = instance if not error else {'error': error}
            if method == GET:
                status_code = success_status_code if instance else 404 if not error else error_status_code
            if method == POST or method == PUT:
                status_code = success_status_code if not error else error_status_code
            return jsonify(response), status_code
        return wrapper
    return decorator
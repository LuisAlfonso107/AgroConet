from functools import wraps
from flask import g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.core.exceptions import UnauthorizedError


def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        if user_id is None:
            raise UnauthorizedError('Token no proporcionado o invalido')
        g.current_user_id = user_id
        return fn(*args, **kwargs)
    return wrapper

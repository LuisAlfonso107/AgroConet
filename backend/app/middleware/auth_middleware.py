from functools import wraps
from flask import g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.core.exceptions import UnauthorizedError


def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        if user_id is None:
            raise UnauthorizedError('Token no proporcionado o invalido')
        claims = get_jwt()
        g.current_user_id = user_id
        g.current_user_type = claims.get('user_type')
        return fn(*args, **kwargs)
    return wrapper

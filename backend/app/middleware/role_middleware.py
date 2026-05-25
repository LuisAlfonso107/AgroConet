from functools import wraps
from flask import g
from app.core.exceptions import ForbiddenError


def require_role(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_type = getattr(g, 'current_user_type', None)
            if user_type not in roles:
                raise ForbiddenError('No tienes permisos para realizar esta accion')
            return fn(*args, **kwargs)
        return wrapper
    return decorator

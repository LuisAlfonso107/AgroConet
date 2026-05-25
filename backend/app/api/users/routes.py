from flask import Blueprint
from app.middleware.auth_middleware import jwt_required_custom
from app.api.users.controllers.user_controller import get_me, update_me, change_password

users_bp = Blueprint('users', __name__)

users_bp.add_url_rule('/api/users/me', view_func=jwt_required_custom(get_me), methods=['GET'])
users_bp.add_url_rule('/api/users/me', view_func=jwt_required_custom(update_me), methods=['PATCH'])
users_bp.add_url_rule('/api/users/me/password', view_func=jwt_required_custom(change_password), methods=['PATCH'])

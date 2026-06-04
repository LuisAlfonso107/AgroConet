from flask import Blueprint
from app.middleware.auth_middleware import jwt_required_custom
from app.api.auth.controllers.auth_controller import register, login, refresh, logout

auth_bp = Blueprint('auth', __name__)

auth_bp.add_url_rule('/api/auth/register', view_func=register, methods=['POST'])
auth_bp.add_url_rule('/api/auth/login', view_func=login, methods=['POST'])
auth_bp.add_url_rule('/api/auth/refresh', view_func=jwt_required_custom(refresh), methods=['POST'])
auth_bp.add_url_rule('/api/auth/logout', view_func=jwt_required_custom(logout), methods=['POST'])

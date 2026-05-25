from flask import Blueprint
from app.middleware.auth_middleware import jwt_required_custom
from app.api.dashboard.controllers.dashboard_controller import resumen

dashboard_bp = Blueprint('dashboard', __name__)

dashboard_bp.add_url_rule('/api/dashboard/resumen', view_func=jwt_required_custom(resumen), methods=['GET'])

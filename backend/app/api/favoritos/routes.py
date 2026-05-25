from flask import Blueprint
from app.middleware.auth_middleware import jwt_required_custom
from app.middleware.role_middleware import require_role
from app.api.favoritos.controllers.favorito_controller import listar, agregar, eliminar

favoritos_bp = Blueprint('favoritos', __name__)

favoritos_bp.add_url_rule(
    '/api/favoritos',
    view_func=jwt_required_custom(require_role('comprador')(listar)),
    methods=['GET'],
)
favoritos_bp.add_url_rule(
    '/api/favoritos',
    view_func=jwt_required_custom(require_role('comprador')(agregar)),
    methods=['POST'],
)
favoritos_bp.add_url_rule(
    '/api/favoritos/<favorito_id>',
    view_func=jwt_required_custom(require_role('comprador')(eliminar)),
    methods=['DELETE'],
)

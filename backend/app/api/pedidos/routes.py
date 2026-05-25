from flask import Blueprint
from app.middleware.auth_middleware import jwt_required_custom
from app.middleware.role_middleware import require_role
from app.api.pedidos.controllers.pedido_controller import (
    listar, get_by_id, crear_pedido, cambiar_estado, cancelar,
)

pedidos_bp = Blueprint('pedidos', __name__)

pedidos_bp.add_url_rule('/api/pedidos', view_func=jwt_required_custom(listar), methods=['GET'])
pedidos_bp.add_url_rule('/api/pedidos/<pedido_id>', view_func=jwt_required_custom(get_by_id), methods=['GET'])
pedidos_bp.add_url_rule(
    '/api/pedidos',
    view_func=jwt_required_custom(require_role('comprador')(crear_pedido)),
    methods=['POST'],
)
pedidos_bp.add_url_rule(
    '/api/pedidos/<pedido_id>/estado',
    view_func=jwt_required_custom(cambiar_estado),
    methods=['PATCH'],
)
pedidos_bp.add_url_rule(
    '/api/pedidos/<pedido_id>',
    view_func=jwt_required_custom(require_role('comprador')(cancelar)),
    methods=['DELETE'],
)

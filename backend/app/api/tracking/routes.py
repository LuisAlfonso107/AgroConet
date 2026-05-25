from flask import Blueprint
from app.middleware.auth_middleware import jwt_required_custom
from app.api.tracking.controllers.tracking_controller import listar_por_pedido, agregar_evento

tracking_bp = Blueprint('tracking', __name__)

tracking_bp.add_url_rule(
    '/api/pedidos/<pedido_id>/tracking',
    view_func=jwt_required_custom(listar_por_pedido),
    methods=['GET'],
)
tracking_bp.add_url_rule(
    '/api/pedidos/<pedido_id>/tracking',
    view_func=jwt_required_custom(agregar_evento),
    methods=['POST'],
)

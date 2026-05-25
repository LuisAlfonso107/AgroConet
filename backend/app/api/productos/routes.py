from flask import Blueprint
from app.middleware.auth_middleware import jwt_required_custom
from app.middleware.role_middleware import require_role
from app.api.productos.controllers.producto_controller import (
    listar, get_by_id, crear, actualizar, eliminar,
)

productos_bp = Blueprint('productos', __name__)

productos_bp.add_url_rule('/api/productos', view_func=listar, methods=['GET'])
productos_bp.add_url_rule('/api/productos/<producto_id>', view_func=get_by_id, methods=['GET'])
productos_bp.add_url_rule(
    '/api/productos',
    view_func=jwt_required_custom(require_role('productor')(crear)),
    methods=['POST'],
)
productos_bp.add_url_rule(
    '/api/productos/<producto_id>',
    view_func=jwt_required_custom(require_role('productor')(actualizar)),
    methods=['PATCH'],
)
productos_bp.add_url_rule(
    '/api/productos/<producto_id>',
    view_func=jwt_required_custom(require_role('productor')(eliminar)),
    methods=['DELETE'],
)

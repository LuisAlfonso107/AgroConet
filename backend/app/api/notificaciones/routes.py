from flask import Blueprint
from app.middleware.auth_middleware import jwt_required_custom
from app.api.notificaciones.controllers.notificacion_controller import listar, marcar_leida

notificaciones_bp = Blueprint('notificaciones', __name__)

notificaciones_bp.add_url_rule('/api/notificaciones', view_func=jwt_required_custom(listar), methods=['GET'])
notificaciones_bp.add_url_rule(
    '/api/notificaciones/<notificacion_id>',
    view_func=jwt_required_custom(marcar_leida),
    methods=['PATCH'],
)

from flask import Blueprint
from app.api.mensajes.controllers.mensaje_controller import crear

mensajes_bp = Blueprint('mensajes', __name__)

mensajes_bp.add_url_rule('/api/contacto-general', view_func=crear, methods=['POST'])

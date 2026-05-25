from flask import Blueprint
from app.middleware.auth_middleware import jwt_required_custom
from app.api.contactos.controllers.contacto_controller import listar, crear

contactos_bp = Blueprint('contactos', __name__)

contactos_bp.add_url_rule('/api/contactos', view_func=jwt_required_custom(listar), methods=['GET'])
contactos_bp.add_url_rule('/api/contactos', view_func=jwt_required_custom(crear), methods=['POST'])

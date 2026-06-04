from flask import request, g
from app.core.responses import success_response, error_response
from app.api.contactos.services import ContactoService
from app.api.contactos.schemas import ContactoSchema

contacto_service = ContactoService()
contacto_schema = ContactoSchema()


def listar():
    contactos = contacto_service.listar(usuario_id=g.current_user_id)
    return success_response(contacto_schema.dump(contactos, many=True))


def crear():
    data = request.get_json()
    contacto = contacto_service.crear(data, g.current_user_id)
    return success_response(contacto_schema.dump(contacto), status=201, message='Consulta enviada exitosamente')

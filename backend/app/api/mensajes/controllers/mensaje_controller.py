from flask import request
from app.core.responses import success_response, error_response
from app.api.mensajes.services import MensajeService
from app.api.mensajes.schemas import MensajeContactoSchema

mensaje_service = MensajeService()
mensaje_schema = MensajeContactoSchema()


def crear():
    data = request.get_json()
    mensaje = mensaje_service.crear(data)
    return success_response(mensaje_schema.dump(mensaje), status=201, message='Mensaje enviado exitosamente')

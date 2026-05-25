from flask import request
from app.core.responses import success_response, error_response
from app.api.mensajes.services import MensajeService

mensaje_service = MensajeService()


def crear():
    data = request.get_json()
    mensaje = mensaje_service.crear(data)
    return success_response(mensaje, status=201, message='Mensaje enviado exitosamente')

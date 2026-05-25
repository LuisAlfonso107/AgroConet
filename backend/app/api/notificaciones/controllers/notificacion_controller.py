from flask import request, g
from app.core.responses import success_response, error_response
from app.api.notificaciones.services import NotificacionService

notificacion_service = NotificacionService()


def listar():
    notificaciones = notificacion_service.listar(g.current_user_id)
    return success_response(notificaciones)


def marcar_leida(notificacion_id):
    notificacion = notificacion_service.marcar_leida(notificacion_id)
    return success_response(notificacion, message='Notificacion marcada como leida')

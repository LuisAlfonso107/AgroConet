from flask import request, g
from app.core.responses import success_response, error_response
from app.api.notificaciones.services import NotificacionService
from app.api.notificaciones.schemas import NotificacionSchema

notificacion_service = NotificacionService()
notificacion_schema = NotificacionSchema()


def listar():
    notificaciones = notificacion_service.listar(g.current_user_id)
    return success_response(notificacion_schema.dump(notificaciones, many=True))


def marcar_leida(notificacion_id):
    notificacion = notificacion_service.marcar_leida(notificacion_id)
    return success_response(notificacion_schema.dump(notificacion), message='Notificacion marcada como leida')

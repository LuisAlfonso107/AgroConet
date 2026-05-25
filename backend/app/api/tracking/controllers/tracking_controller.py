from flask import request, g
from app.core.responses import success_response, error_response
from app.api.tracking.services import TrackingService

tracking_service = TrackingService()


def listar_por_pedido(pedido_id):
    order = request.args.get('_order', 'asc')
    eventos = tracking_service.listar_por_pedido(pedido_id, order=order)
    return success_response(eventos)


def agregar_evento(pedido_id):
    data = request.get_json()
    evento = tracking_service.agregar_evento(pedido_id, g.current_user_id, data)
    return success_response(evento, status=201, message='Evento agregado exitosamente')

from flask import request, g
from app.core.responses import success_response, error_response
from app.api.pedidos.services import PedidoService

pedido_service = PedidoService()


def listar():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    result = pedido_service.listar(page=page, limit=limit, user_id=g.current_user_id)
    return success_response(result)


def get_by_id(pedido_id):
    pedido = pedido_service.get_by_id(pedido_id)
    return success_response(pedido)


def crear_pedido():
    data = request.get_json()
    pedido = pedido_service.crear_pedido(data, g.current_user_id)
    return success_response(pedido, status=201, message='Pedido creado exitosamente')


def cambiar_estado(pedido_id):
    data = request.get_json()
    pedido = pedido_service.cambiar_estado(pedido_id, data.get('estado'))
    return success_response(pedido, message='Estado actualizado exitosamente')


def cancelar(pedido_id):
    result = pedido_service.cancelar(pedido_id)
    return success_response(result, message='Pedido cancelado exitosamente')

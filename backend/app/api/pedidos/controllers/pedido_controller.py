from flask import request, g
from marshmallow import ValidationError
from app.core.responses import success_response, error_response
from app.api.pedidos.services import PedidoService
from app.api.pedidos.schemas import PedidoSchema, PedidoCreateSchema, EstadoUpdateSchema

pedido_service = PedidoService()
pedido_schema = PedidoSchema()
create_schema = PedidoCreateSchema()
estado_schema = EstadoUpdateSchema()


def listar():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    estado_filtro = request.args.get('estado')
    result = pedido_service.listar(
        page=page, limit=limit, user_id=g.current_user_id
    )
    if estado_filtro:
        result['data'] = [p for p in result['data'] if p.estado == estado_filtro]
        result['meta']['total'] = len(result['data'])
    from flask import jsonify
    return jsonify({
        'data': pedido_schema.dump(result['data'], many=True),
        'meta': result['meta'],
        'message': 'Success',
    })


def get_by_id(pedido_id):
    pedido = pedido_service.get_by_id(pedido_id)
    return success_response(pedido_schema.dump(pedido))


def crear_pedido():
    data = request.get_json()
    try:
        validated = create_schema.load(data)
    except ValidationError as err:
        return error_response(err.messages, 400)
    pedido = pedido_service.crear_pedido(validated, g.current_user_id)
    return success_response(pedido_schema.dump(pedido), status=201, message='Pedido creado exitosamente')


def cambiar_estado(pedido_id):
    data = request.get_json()
    try:
        validated = estado_schema.load(data)
    except ValidationError as err:
        return error_response(err.messages, 400)
    pedido = pedido_service.cambiar_estado(pedido_id, validated['estado'])
    return success_response(pedido_schema.dump(pedido), message='Estado actualizado exitosamente')


def cancelar(pedido_id):
    result = pedido_service.cancelar(pedido_id)
    return success_response(result, message='Pedido cancelado exitosamente')

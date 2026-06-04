from flask import request, g
from marshmallow import ValidationError
from app.core.responses import success_response, error_response
from app.api.productos.services import ProductoService
from app.api.productos.schemas import ProductoSchema, ProductoCreateSchema, ProductoUpdateSchema

producto_service = ProductoService()
producto_schema = ProductoSchema()
create_schema = ProductoCreateSchema()
update_schema = ProductoUpdateSchema()


def listar():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    filters = {k: v for k, v in request.args.items() if k not in ('page', 'limit')}
    result = producto_service.listar(page=page, limit=limit, filters=filters)
    from flask import jsonify
    return jsonify({
        'data': producto_schema.dump(result['data'], many=True),
        'meta': result['meta'],
        'message': 'Success',
    })


def get_by_id(producto_id):
    producto = producto_service.get_by_id(producto_id)
    return success_response(producto_schema.dump(producto))


def crear():
    data = request.get_json()
    try:
        validated = create_schema.load(data)
    except ValidationError as err:
        return error_response(err.messages, 400)
    producto = producto_service.crear(validated, g.current_user_id)
    return success_response(producto_schema.dump(producto), status=201, message='Producto creado exitosamente')


def actualizar(producto_id):
    data = request.get_json()
    try:
        validated = update_schema.load(data)
    except ValidationError as err:
        return error_response(err.messages, 400)
    producto = producto_service.actualizar(producto_id, validated)
    return success_response(producto_schema.dump(producto), message='Producto actualizado exitosamente')


def eliminar(producto_id):
    producto_service.eliminar(producto_id)
    return success_response(None, message='Producto eliminado exitosamente')

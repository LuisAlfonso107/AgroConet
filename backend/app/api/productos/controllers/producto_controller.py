from flask import request, g
from app.core.responses import success_response, error_response
from app.api.productos.services import ProductoService

producto_service = ProductoService()


def listar():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    filters = request.args.to_dict()
    result = producto_service.listar(page=page, limit=limit, filters=filters)
    return success_response(result)


def get_by_id(producto_id):
    producto = producto_service.get_by_id(producto_id)
    return success_response(producto)


def crear():
    data = request.get_json()
    producto = producto_service.crear(data, g.current_user_id)
    return success_response(producto, status=201, message='Producto creado exitosamente')


def actualizar(producto_id):
    data = request.get_json()
    producto = producto_service.actualizar(producto_id, data)
    return success_response(producto, message='Producto actualizado exitosamente')


def eliminar(producto_id):
    producto_service.eliminar(producto_id)
    return success_response(None, message='Producto eliminado exitosamente')

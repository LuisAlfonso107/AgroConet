from flask import request, g
from app.core.responses import success_response, error_response
from app.api.favoritos.services import FavoritoService

favorito_service = FavoritoService()


def listar():
    favoritos = favorito_service.listar(g.current_user_id)
    return success_response(favoritos)


def agregar():
    data = request.get_json()
    favorito = favorito_service.agregar(g.current_user_id, data.get('producto_id'))
    return success_response(favorito, status=201, message='Favorito agregado exitosamente')


def eliminar(favorito_id):
    favorito_service.eliminar(favorito_id)
    return success_response(None, message='Favorito eliminado exitosamente')

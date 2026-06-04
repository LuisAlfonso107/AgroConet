from flask import request, g
from marshmallow import ValidationError
from app.core.responses import success_response, error_response
from app.api.auth.services import AuthService
from app.api.auth.schemas import RegisterSchema, LoginSchema

auth_service = AuthService()
register_schema = RegisterSchema()
login_schema = LoginSchema()


def register():
    data = request.get_json()
    try:
        validated = register_schema.load(data)
    except ValidationError as err:
        return error_response(err.messages, 400)
    result = auth_service.register(validated)
    return success_response(result, status=201, message='Usuario registrado exitosamente')


def login():
    data = request.get_json()
    try:
        validated = login_schema.load(data)
    except ValidationError as err:
        return error_response(err.messages, 400)
    result = auth_service.login(validated)
    return success_response(result, message='Inicio de sesion exitoso')


def refresh():
    if not hasattr(g, 'current_user_id') or not g.current_user_id:
        return error_response('Token de refresco no proporcionado o invalido', 401)
    result = auth_service.refresh_token(g.current_user_id)
    return success_response(result, message='Token renovado exitosamente')


def logout():
    if not hasattr(g, 'current_user_id') or not g.current_user_id:
        return error_response('Token no proporcionado', 401)
    result = auth_service.logout(g.current_user_id)
    return success_response(result, message='Sesion cerrada exitosamente')

from flask import request, g
from app.core.responses import success_response, error_response
from app.api.auth.services import AuthService

auth_service = AuthService()


def register():
    data = request.get_json()
    result = auth_service.register(data)
    return success_response(result, status=201, message='Usuario registrado exitosamente')


def login():
    data = request.get_json()
    result = auth_service.login(data)
    return success_response(result, message='Inicio de sesion exitoso')


def refresh():
    result = auth_service.refresh_token(g.current_user_id)
    return success_response(result, message='Token renovado exitosamente')


def logout():
    result = auth_service.logout(g.current_user_id)
    return success_response(result, message='Sesion cerrada exitosamente')

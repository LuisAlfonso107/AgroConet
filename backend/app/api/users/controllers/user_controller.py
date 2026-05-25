from flask import request, g
from app.core.responses import success_response, error_response
from app.api.users.services import UserService

user_service = UserService()


def get_me():
    user = user_service.get_me(g.current_user_id)
    return success_response(user)


def update_me():
    data = request.get_json()
    user = user_service.update_me(g.current_user_id, data)
    return success_response(user, message='Perfil actualizado exitosamente')


def change_password():
    data = request.get_json()
    result = user_service.change_password(
        g.current_user_id,
        data.get('current_password'),
        data.get('new_password'),
    )
    return success_response(result, message='Contrasena cambiada exitosamente')

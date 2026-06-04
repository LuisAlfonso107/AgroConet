from flask import request, g
from app.core.responses import success_response, error_response
from app.api.users.services import UserService
from app.api.users.schemas import UserSchema

user_service = UserService()
user_schema = UserSchema()


def get_me():
    user = user_service.get_me(g.current_user_id)
    return success_response(user_schema.dump(user))


def update_me():
    data = request.get_json()
    user = user_service.update_me(g.current_user_id, data)
    return success_response(user_schema.dump(user), message='Perfil actualizado exitosamente')


def change_password():
    data = request.get_json()
    result = user_service.change_password(
        g.current_user_id,
        data.get('current_password'),
        data.get('new_password'),
    )
    return success_response(result, message='Contrasena cambiada exitosamente')

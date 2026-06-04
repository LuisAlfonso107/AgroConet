from app.extensions import db, bcrypt
from app.api.users.models import User
from app.core.exceptions import NotFoundError, UnauthorizedError


class UserService:

    def get_me(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('Usuario no encontrado')
        return user

    def update_me(self, user_id, data):
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('Usuario no encontrado')

        allowed_fields = [
            'name', 'telefono', 'foto_perfil', 'empresa', 'direccion_envio',
            'direcciones_envio', 'pais', 'preferencias_notificacion', 'finca',
            'ubicacion', 'descripcion',
        ]
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        db.session.commit()
        return user

    def change_password(self, user_id, current_password, new_password):
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('Usuario no encontrado')

        if not bcrypt.check_password_hash(user.password, current_password):
            raise UnauthorizedError('La contraseña actual no es correcta')

        user.password = bcrypt.generate_password_hash(new_password, rounds=12).decode('utf-8')
        db.session.commit()
        return {'message': 'Contraseña cambiada exitosamente'}

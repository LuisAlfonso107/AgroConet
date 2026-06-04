import uuid
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import db, bcrypt
from app.api.users.models import User
from app.core.exceptions import ConflictError, UnauthorizedError, UnprocessableError


class AuthService:

    def register(self, data):
        email = data.get('email', '').lower().strip()
        existing = User.query.filter_by(email=email).first()
        if existing:
            raise ConflictError('El email ya está registrado')

        password_hash = bcrypt.generate_password_hash(data['password'], rounds=12).decode('utf-8')

        user = User(
            id=str(uuid.uuid4()),
            name=data['name'],
            email=email,
            password=password_hash,
            user_type=data['user_type'],
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ConflictError('El email ya está registrado')

        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'user_type': user.user_type,
        }

    def login(self, data):
        email = data.get('email', '').lower().strip()
        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(user.password, data.get('password', '')):
            raise UnauthorizedError('Credenciales inválidas')

        access_token = create_access_token(
            identity=user.id,
            additional_claims={'user_type': user.user_type},
        )
        refresh_token = create_refresh_token(identity=user.id)

        user.refresh_token = refresh_token
        db.session.commit()

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'user_type': user.user_type,
            },
        }

    def refresh_token(self, identity):
        user = User.query.get(identity)
        if not user:
            raise UnauthorizedError('Usuario no encontrado')

        access_token = create_access_token(
            identity=user.id,
            additional_claims={'user_type': user.user_type},
        )
        return {'access_token': access_token}

    def logout(self, identity):
        user = User.query.get(identity)
        if user:
            user.refresh_token = None
            db.session.commit()
        return {'message': 'Sesión cerrada exitosamente'}

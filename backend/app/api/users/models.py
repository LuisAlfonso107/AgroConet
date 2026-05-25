import uuid
from datetime import datetime, timezone
from app.extensions import db


class UserType:
    COMPRADOR = 'comprador'
    PRODUCTOR = 'productor'
    AGENCIA = 'agencia'


user_types = (UserType.COMPRADOR, UserType.PRODUCTOR, UserType.AGENCIA)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(20))
    foto_perfil = db.Column(db.String(500))
    empresa = db.Column(db.String(200))
    direccion_envio = db.Column(db.String(300))
    direcciones_envio = db.Column(db.JSON)
    pais = db.Column(db.String(100))
    preferencias_notificacion = db.Column(db.JSON)
    finca = db.Column(db.String(200))
    ubicacion = db.Column(db.String(300))
    descripcion = db.Column(db.Text)
    refresh_token = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())

    productos = db.relationship('Producto', backref='productor_user', lazy='dynamic')
    favoritos = db.relationship('Favorito', backref='comprador_user', lazy='dynamic', foreign_keys='Favorito.comprador_id')
    contactos = db.relationship('Contacto', backref='usuario', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'

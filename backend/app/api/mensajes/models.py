from datetime import datetime, timezone
from app.extensions import db


class MensajeEstado:
    NUEVO = 'nuevo'
    LEIDO = 'leido'
    RESPONDIDO = 'respondido'


mensaje_estados = (MensajeEstado.NUEVO, MensajeEstado.LEIDO, MensajeEstado.RESPONDIDO)


class MensajeContacto(db.Model):
    __tablename__ = 'mensajes_contacto'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20))
    asunto = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default=MensajeEstado.NUEVO)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    def __repr__(self):
        return f'<MensajeContacto {self.id}>'

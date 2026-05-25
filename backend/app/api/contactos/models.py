from datetime import datetime, timezone
from app.extensions import db


class ContactoEstado:
    PENDIENTE = 'pendiente'
    LEIDO = 'leido'
    RESPONDIDO = 'respondido'
    CERRADO = 'cerrado'


contacto_estados = (ContactoEstado.PENDIENTE, ContactoEstado.LEIDO, ContactoEstado.RESPONDIDO, ContactoEstado.CERRADO)


class Contacto(db.Model):
    __tablename__ = 'contactos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    usuario_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    producto_id = db.Column(db.String(36), db.ForeignKey('productos.id'), nullable=True)
    productor = db.Column(db.String(200))
    mensaje = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default=ContactoEstado.PENDIENTE)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    def __repr__(self):
        return f'<Contacto {self.id}>'

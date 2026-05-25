from datetime import datetime, timezone
from app.extensions import db


class NotificacionTipo:
    PEDIDO = 'pedido'
    MENSAJE = 'mensaje'
    SISTEMA = 'sistema'
    PROMOCION = 'promocion'


notificacion_tipos = (NotificacionTipo.PEDIDO, NotificacionTipo.MENSAJE, NotificacionTipo.SISTEMA, NotificacionTipo.PROMOCION)


class Notificacion(db.Model):
    __tablename__ = 'notificaciones'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    usuario_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    leida = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    usuario = db.relationship('User', backref='notificaciones', lazy='joined')

    def __repr__(self):
        return f'<Notificacion {self.id}>'

from datetime import datetime, timezone
from app.extensions import db


class PedidoEstado:
    SOLICITADO = 'solicitado'
    CONFIRMADO = 'confirmado'
    EN_PUERTO = 'en puerto'
    EN_TRANSITO = 'en transito'
    ENTREGADO = 'entregado'
    RECHAZADO = 'rechazado'
    CANCELADO = 'cancelado'


pedido_estados = (
    PedidoEstado.SOLICITADO,
    PedidoEstado.CONFIRMADO,
    PedidoEstado.EN_PUERTO,
    PedidoEstado.EN_TRANSITO,
    PedidoEstado.ENTREGADO,
    PedidoEstado.RECHAZADO,
    PedidoEstado.CANCELADO,
)


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    producto_id = db.Column(db.String(36), db.ForeignKey('productos.id'), nullable=False)
    comprador_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    productor_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    agencia_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    nombre_producto = db.Column(db.String(200), nullable=False)
    cantidad_quintales = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default=PedidoEstado.SOLICITADO)
    impuestos = db.Column(db.Float)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())

    comprador = db.relationship('User', backref='pedidos_comprador', lazy='joined', foreign_keys=[comprador_id])
    productor = db.relationship('User', backref='pedidos_productor', lazy='joined', foreign_keys=[productor_id])
    agencia = db.relationship('User', backref='pedidos_agencia', lazy='joined', foreign_keys=[agencia_id])
    tracking_eventos = db.relationship('TrackingEvento', backref='pedido_rel', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Pedido {self.id}>'

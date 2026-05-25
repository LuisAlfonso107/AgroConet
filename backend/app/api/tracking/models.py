from datetime import datetime, timezone
from app.extensions import db
from app.api.pedidos.models import PedidoEstado


class TrackingEvento(db.Model):
    __tablename__ = 'tracking_eventos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    pedido_id = db.Column(db.String(36), db.ForeignKey('pedidos.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    estado = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    user = db.relationship('User', backref='tracking_eventos', lazy='joined')

    def __repr__(self):
        return f'<TrackingEvento {self.id} pedido={self.pedido_id}>'

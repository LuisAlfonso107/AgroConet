from datetime import datetime, timezone
from app.extensions import db


class Favorito(db.Model):
    __tablename__ = 'favoritos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    comprador_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    producto_id = db.Column(db.String(36), db.ForeignKey('productos.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint('comprador_id', 'producto_id', name='uq_favorito_comprador_producto'),
    )

    def __repr__(self):
        return f'<Favorito {self.comprador_id} -> {self.producto_id}>'

from datetime import datetime, timezone
from app.extensions import db


class ProductoTipo:
    CAFE = 'cafe'
    MAIZ = 'maiz'
    FRIJOL = 'frijol'
    ARROZ = 'arroz'
    OTROS = 'otros'


producto_tipos = (ProductoTipo.CAFE, ProductoTipo.MAIZ, ProductoTipo.FRIJOL, ProductoTipo.ARROZ, ProductoTipo.OTROS)


class ProductoEstado:
    DISPONIBLE = 'disponible'
    AGOTADO = 'agotado'
    PAUSADO = 'pausado'


producto_estados = (ProductoEstado.DISPONIBLE, ProductoEstado.AGOTADO, ProductoEstado.PAUSADO)


class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    nombre = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    estado = db.Column(db.String(20), nullable=False, default=ProductoEstado.DISPONIBLE)
    productor_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    humedad = db.Column(db.Float, nullable=False)
    variedad = db.Column(db.String(200), nullable=False)
    region = db.Column(db.String(200), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    altura = db.Column(db.String(50), nullable=False)
    certificaciones = db.Column(db.JSON, default=list)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(500))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    pedidos = db.relationship('Pedido', backref='producto_rel', lazy='dynamic')
    favoritos = db.relationship('Favorito', backref='producto_rel', lazy='dynamic')
    contactos = db.relationship('Contacto', backref='producto_rel', lazy='dynamic')

    def __repr__(self):
        return f'<Producto {self.nombre}>'

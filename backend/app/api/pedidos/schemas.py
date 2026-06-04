from marshmallow import fields, validate
from app.extensions import ma
from app.api.pedidos.models import Pedido


class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pedido
        load_instance = True
        include_fk = True

    estado = fields.String(validate=validate.OneOf([
        'solicitado', 'confirmado', 'en puerto', 'en transito',
        'entregado', 'rechazado', 'cancelado',
    ]))


class PedidoCreateSchema(ma.Schema):
    producto_id = fields.String(required=True)
    nombre_producto = fields.String(required=True)
    cantidad_quintales = fields.Float(required=True)
    precio_unitario = fields.Float(required=True)
    total = fields.Float(required=True)


class EstadoUpdateSchema(ma.Schema):
    estado = fields.String(required=True, validate=validate.OneOf([
        'solicitado', 'confirmado', 'en puerto', 'en transito',
        'entregado', 'rechazado', 'cancelado',
    ]))

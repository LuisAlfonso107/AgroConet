from marshmallow import fields, validate
from app.extensions import ma
from app.api.tracking.models import TrackingEvento


class TrackingEventoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrackingEvento
        load_instance = True
        include_fk = True

    estado = fields.String(validate=validate.OneOf([
        'solicitado', 'confirmado', 'en puerto', 'en transito',
        'entregado', 'rechazado', 'cancelado',
    ]))


class TrackingCreateSchema(ma.Schema):
    estado = fields.String(required=True, validate=validate.OneOf([
        'solicitado', 'confirmado', 'en puerto', 'en transito',
        'entregado', 'rechazado', 'cancelado',
    ]))
    descripcion = fields.String(required=True)

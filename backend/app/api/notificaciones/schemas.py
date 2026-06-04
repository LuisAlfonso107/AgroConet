from marshmallow import fields, validate
from app.extensions import ma
from app.api.notificaciones.models import Notificacion


class NotificacionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notificacion
        load_instance = True
        include_fk = True

    tipo = fields.String(validate=validate.OneOf(['pedido', 'mensaje', 'sistema', 'promocion']))

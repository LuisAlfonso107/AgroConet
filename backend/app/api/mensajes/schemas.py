from marshmallow import fields, validate
from app.extensions import ma


class MensajeContactoSchema(ma.SQLAlchemyAutoSchema):
    from app.api.mensajes.models import MensajeContacto

    class Meta:
        model = MensajeContacto
        load_instance = True

    estado = fields.String(validate=validate.OneOf(['nuevo', 'leido', 'respondido']))


class MensajeCreateSchema(ma.Schema):
    nombre = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    telefono = fields.String()
    asunto = fields.String(required=True)
    mensaje = fields.String(required=True)

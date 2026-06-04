from marshmallow import fields, validate
from app.extensions import ma
from app.api.contactos.models import Contacto


class ContactoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Contacto
        load_instance = True
        include_fk = True

    estado = fields.String(validate=validate.OneOf(['pendiente', 'leido', 'respondido', 'cerrado']))


class ContactoCreateSchema(ma.Schema):
    producto_id = fields.String()
    mensaje = fields.String(required=True)

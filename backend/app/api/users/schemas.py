from marshmallow import fields, validate
from app.extensions import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    from app.api.users.models import User

    class Meta:
        model = User
        exclude = ('password', 'refresh_token')
        load_instance = True

    user_type = fields.String(validate=validate.OneOf(['comprador', 'productor', 'agencia']))


class UserUpdateSchema(ma.Schema):
    name = fields.String()
    telefono = fields.String()
    foto_perfil = fields.String()
    empresa = fields.String()
    direccion_envio = fields.String()
    direcciones_envio = fields.List(fields.String())
    pais = fields.String()
    preferencias_notificacion = fields.Dict()
    finca = fields.String()
    ubicacion = fields.String()
    descripcion = fields.String()


class PasswordChangeSchema(ma.Schema):
    current_password = fields.String(required=True)
    new_password = fields.String(required=True, validate=validate.Length(min=6))

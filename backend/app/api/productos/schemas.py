from marshmallow import fields, validate
from app.extensions import ma
from app.api.productos.models import Producto


class ProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        load_instance = True

    tipo = fields.String(validate=validate.OneOf(['cafe', 'maiz', 'frijol', 'arroz', 'otros']))
    estado = fields.String(validate=validate.OneOf(['disponible', 'agotado', 'pausado']))


class ProductoCreateSchema(ma.Schema):
    nombre = fields.String(required=True, validate=validate.Length(min=1))
    tipo = fields.String(required=True, validate=validate.OneOf(['cafe', 'maiz', 'frijol', 'arroz', 'otros']))
    precio = fields.Float(required=True)
    stock = fields.Integer(required=True)
    humedad = fields.Float(required=True)
    variedad = fields.String(required=True)
    region = fields.String(required=True)
    pais = fields.String(required=True)
    altura = fields.String(required=True)
    certificaciones = fields.List(fields.String())
    descripcion = fields.String()
    imagen = fields.String()
    lat = fields.Float()
    lon = fields.Float()


class ProductoUpdateSchema(ma.Schema):
    nombre = fields.String()
    tipo = fields.String(validate=validate.OneOf(['cafe', 'maiz', 'frijol', 'arroz', 'otros']))
    precio = fields.Float()
    stock = fields.Integer()
    estado = fields.String(validate=validate.OneOf(['disponible', 'agotado', 'pausado']))
    humedad = fields.Float()
    variedad = fields.String()
    region = fields.String()
    pais = fields.String()
    altura = fields.String()
    certificaciones = fields.List(fields.String())
    descripcion = fields.String()
    imagen = fields.String()
    lat = fields.Float()
    lon = fields.Float()

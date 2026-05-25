from marshmallow import fields
from app.extensions import ma
from app.api.productos.schemas import ProductoSchema


class FavoritoSchema(ma.SQLAlchemyAutoSchema):
    from app.api.favoritos.models import Favorito

    class Meta:
        model = Favorito
        load_instance = True
        include_fk = True

    producto = fields.Nested(ProductoSchema)

from app.extensions import db
from app.api.favoritos.models import Favorito
from app.api.productos.models import Producto
from app.core.exceptions import NotFoundError, ConflictError


class FavoritoService:

    def listar(self, comprador_id):
        return Favorito.query.filter_by(comprador_id=comprador_id).all()

    def agregar(self, comprador_id, producto_id):
        producto = Producto.query.get(producto_id)
        if not producto:
            raise NotFoundError('Producto no encontrado')

        existente = Favorito.query.filter_by(
            comprador_id=comprador_id, producto_id=producto_id
        ).first()
        if existente:
            raise ConflictError('El producto ya está en favoritos')

        favorito = Favorito(comprador_id=comprador_id, producto_id=producto_id)
        db.session.add(favorito)
        db.session.commit()
        return favorito

    def eliminar(self, favorito_id):
        favorito = Favorito.query.get(favorito_id)
        if not favorito:
            raise NotFoundError('Favorito no encontrado')
        db.session.delete(favorito)
        db.session.commit()

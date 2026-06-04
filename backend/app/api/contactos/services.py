from app.extensions import db
from app.api.contactos.models import Contacto
from app.api.productos.models import Producto
from app.core.exceptions import NotFoundError


class ContactoService:

    def listar(self, usuario_id=None):
        query = Contacto.query
        if usuario_id:
            query = query.filter_by(usuario_id=usuario_id)
        return query.order_by(Contacto.created_at.desc()).all()

    def crear(self, data, usuario_id):
        producto_id = data.get('producto_id')
        if producto_id:
            producto = Producto.query.get(producto_id)
            if not producto:
                raise NotFoundError('Producto no encontrado')

        contacto = Contacto(
            usuario_id=usuario_id,
            producto_id=producto_id,
            mensaje=data['mensaje'],
        )
        db.session.add(contacto)
        db.session.commit()
        return contacto

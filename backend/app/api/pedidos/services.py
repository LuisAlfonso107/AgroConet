from app.extensions import db
from app.api.pedidos.models import Pedido, PedidoEstado
from app.api.productos.models import Producto, ProductoEstado as ProdEstado
from app.api.tracking.models import TrackingEvento
from app.core.exceptions import NotFoundError, UnprocessableError, ForbiddenError
from app.core.pagination import paginate_query

VALID_TRANSITIONS = {
    PedidoEstado.SOLICITADO: [PedidoEstado.CONFIRMADO, PedidoEstado.RECHAZADO, PedidoEstado.CANCELADO],
    PedidoEstado.CONFIRMADO: [PedidoEstado.EN_PUERTO, PedidoEstado.RECHAZADO],
    PedidoEstado.EN_PUERTO: [PedidoEstado.EN_TRANSITO],
    PedidoEstado.EN_TRANSITO: [PedidoEstado.ENTREGADO],
    PedidoEstado.ENTREGADO: [],
    PedidoEstado.RECHAZADO: [],
    PedidoEstado.CANCELADO: [],
}


class PedidoService:

    def listar(self, page=1, limit=20, user_id=None, user_type=None):
        query = Pedido.query

        if user_id:
            query = query.filter(
                db.or_(Pedido.comprador_id == user_id, Pedido.productor_id == user_id)
            )

        query = query.order_by(Pedido.created_at.desc())
        return paginate_query(query, page=page, limit=limit)

    def get_by_id(self, pedido_id):
        pedido = Pedido.query.get(pedido_id)
        if not pedido:
            raise NotFoundError('Pedido no encontrado')
        return pedido

    def crear_pedido(self, data, comprador_id):
        producto = Producto.query.with_for_update().get(data['producto_id'])
        if not producto:
            raise NotFoundError('Producto no encontrado')

        if producto.estado not in (ProdEstado.DISPONIBLE,):
            raise UnprocessableError('Producto no disponible para compra')

        cantidad = float(data['cantidad_quintales'])
        if cantidad > producto.stock:
            raise UnprocessableError(
                f'Stock insuficiente, disponible: {producto.stock} quintales'
            )

        precio_total = cantidad * producto.precio

        import uuid
        pedido = Pedido(
            id=str(uuid.uuid4()),
            producto_id=producto.id,
            comprador_id=comprador_id,
            productor_id=producto.productor_id,
            nombre_producto=producto.nombre,
            cantidad_quintales=cantidad,
            precio_unitario=producto.precio,
            total=precio_total,
            estado=PedidoEstado.SOLICITADO,
        )

        producto.stock -= cantidad
        if producto.stock == 0:
            producto.estado = ProdEstado.AGOTADO

        db.session.add(pedido)

        evento = TrackingEvento(
            pedido_id=pedido.id,
            user_id=comprador_id,
            estado=PedidoEstado.SOLICITADO,
            descripcion='Pedido creado',
        )
        db.session.add(evento)

        db.session.commit()
        return pedido

    def cambiar_estado(self, pedido_id, nuevo_estado):
        pedido = self.get_by_id(pedido_id)

        transiciones_validas = VALID_TRANSITIONS.get(pedido.estado, [])
        if nuevo_estado not in transiciones_validas:
            raise UnprocessableError(
                f'Transición de estado no permitida: {pedido.estado} -> {nuevo_estado}'
            )

        pedido.estado = nuevo_estado
        db.session.add(pedido)

        evento = TrackingEvento(
            pedido_id=pedido.id,
            user_id=None,
            estado=nuevo_estado,
            descripcion=f'Estado cambiado a {nuevo_estado}',
        )
        db.session.add(evento)
        db.session.commit()
        return pedido

    def cancelar(self, pedido_id):
        pedido = self.get_by_id(pedido_id)

        cancelable = [PedidoEstado.SOLICITADO, PedidoEstado.CONFIRMADO]
        if pedido.estado not in cancelable:
            raise UnprocessableError('El pedido no puede ser cancelado en su estado actual')

        pedido.estado = PedidoEstado.CANCELADO

        producto = Producto.query.get(pedido.producto_id)
        if producto:
            producto.stock += int(pedido.cantidad_quintales)
            if producto.estado == ProdEstado.AGOTADO and producto.stock > 0:
                producto.estado = ProdEstado.DISPONIBLE

        evento = TrackingEvento(
            pedido_id=pedido.id,
            user_id=None,
            estado=PedidoEstado.CANCELADO,
            descripcion='Pedido cancelado',
        )
        db.session.add(evento)
        db.session.commit()
        return {'message': 'Pedido cancelado exitosamente'}

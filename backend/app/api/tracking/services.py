from app.extensions import db
from app.api.tracking.models import TrackingEvento
from app.api.pedidos.models import Pedido
from app.core.exceptions import NotFoundError


class TrackingService:

    def listar_por_pedido(self, pedido_id, order='asc'):
        pedido = Pedido.query.get(pedido_id)
        if not pedido:
            raise NotFoundError('Pedido no encontrado')

        query = TrackingEvento.query.filter_by(pedido_id=pedido_id)
        if order == 'asc':
            query = query.order_by(TrackingEvento.created_at.asc())
        else:
            query = query.order_by(TrackingEvento.created_at.desc())
        return query.all()

    def agregar_evento(self, pedido_id, user_id, data):
        pedido = Pedido.query.get(pedido_id)
        if not pedido:
            raise NotFoundError('Pedido no encontrado')

        evento = TrackingEvento(
            pedido_id=pedido_id,
            user_id=user_id,
            estado=data['estado'],
            descripcion=data['descripcion'],
        )
        db.session.add(evento)
        db.session.commit()
        return evento

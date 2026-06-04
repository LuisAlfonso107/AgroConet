from app.extensions import db
from app.api.notificaciones.models import Notificacion
from app.core.exceptions import NotFoundError


class NotificacionService:

    def listar(self, usuario_id):
        return Notificacion.query.filter_by(usuario_id=usuario_id).order_by(
            Notificacion.created_at.desc()
        ).all()

    def marcar_leida(self, notificacion_id):
        notificacion = Notificacion.query.get(notificacion_id)
        if not notificacion:
            raise NotFoundError('Notificación no encontrada')
        notificacion.leida = True
        db.session.commit()
        return notificacion

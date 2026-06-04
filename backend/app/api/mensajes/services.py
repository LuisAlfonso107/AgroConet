from app.extensions import db
from app.api.mensajes.models import MensajeContacto


class MensajeService:

    def crear(self, data):
        mensaje = MensajeContacto(
            nombre=data['nombre'],
            email=data['email'],
            asunto=data.get('asunto', ''),
            mensaje=data['mensaje'],
        )
        db.session.add(mensaje)
        db.session.commit()
        return mensaje

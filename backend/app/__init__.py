import os
from flask import Flask
from .config import config_map
from .extensions import db, jwt, bcrypt, cors, migrate, ma
from .core.error_handlers import register_error_handlers


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*')}})
    migrate.init_app(app, db)
    ma.init_app(app)

    # Import all models so Alembic detects them and relationships resolve
    from app.api.users.models import User
    from app.api.productos.models import Producto
    from app.api.pedidos.models import Pedido
    from app.api.tracking.models import TrackingEvento
    from app.api.favoritos.models import Favorito
    from app.api.contactos.models import Contacto
    from app.api.mensajes.models import MensajeContacto
    from app.api.notificaciones.models import Notificacion

    register_error_handlers(app)

    from app.api import register_blueprints
    register_blueprints(app)

    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'version': '1.0.0'}, 200

    return app

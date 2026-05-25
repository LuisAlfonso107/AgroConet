from flask import Flask


def register_blueprints(app: Flask):
    from app.api.auth.routes import auth_bp
    from app.api.users.routes import users_bp
    from app.api.productos.routes import productos_bp
    from app.api.pedidos.routes import pedidos_bp
    from app.api.tracking.routes import tracking_bp
    from app.api.favoritos.routes import favoritos_bp
    from app.api.contactos.routes import contactos_bp
    from app.api.mensajes.routes import mensajes_bp
    from app.api.notificaciones.routes import notificaciones_bp
    from app.api.dashboard.routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(tracking_bp)
    app.register_blueprint(favoritos_bp)
    app.register_blueprint(contactos_bp)
    app.register_blueprint(mensajes_bp)
    app.register_blueprint(notificaciones_bp)
    app.register_blueprint(dashboard_bp)

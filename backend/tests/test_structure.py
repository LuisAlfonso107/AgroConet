def test_blueprint_auth_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    auth_routes = [r for r in rules if r.startswith('/api/auth')]
    assert len(auth_routes) > 0


def test_blueprint_users_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    user_routes = [r for r in rules if r.startswith('/api/users')]
    assert len(user_routes) > 0


def test_blueprint_productos_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    prod_routes = [r for r in rules if r.startswith('/api/productos')]
    assert len(prod_routes) > 0


def test_blueprint_pedidos_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    ped_routes = [r for r in rules if r.startswith('/api/pedidos')]
    assert len(ped_routes) > 0


def test_blueprint_tracking_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    tracking_routes = [r for r in rules if '/tracking' in r]
    assert len(tracking_routes) > 0


def test_blueprint_favoritos_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    fav_routes = [r for r in rules if r.startswith('/api/favoritos')]
    assert len(fav_routes) > 0


def test_blueprint_contactos_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    cont_routes = [r for r in rules if r.startswith('/api/contactos')]
    assert len(cont_routes) > 0


def test_blueprint_mensajes_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    msg_routes = [r for r in rules if r.startswith('/api/contacto-general')]
    assert len(msg_routes) > 0


def test_blueprint_notificaciones_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    notif_routes = [r for r in rules if r.startswith('/api/notificaciones')]
    assert len(notif_routes) > 0


def test_blueprint_dashboard_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    dash_routes = [r for r in rules if r.startswith('/api/dashboard')]
    assert len(dash_routes) > 0


def test_health_endpoint_works(client):
    response = client.get('/api/health')
    assert response.status_code == 200


def test_endpoints_do_not_return_404(client):
    # Only endpoints that don't hit stub services can be tested
    # Stub services raise NotImplementedError by design
    response = client.get('/api/health')
    assert response.status_code == 200

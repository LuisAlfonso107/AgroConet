def test_app_creates_successfully(app):
    assert app is not None
    assert app.testing is True


def test_health_endpoint_returns_200(client):
    response = client.get('/api/health')
    assert response.status_code == 200


def test_health_endpoint_returns_expected_json(client):
    response = client.get('/api/health')
    data = response.get_json()
    assert data is not None
    assert data.get('status') == 'ok'
    assert data.get('version') == '1.0.0'


def test_extensions_are_initialized(app):
    from app.extensions import db, jwt, bcrypt, cors, migrate, ma
    assert db is not None
    assert jwt is not None
    assert bcrypt is not None
    assert cors is not None
    assert migrate is not None
    assert ma is not None

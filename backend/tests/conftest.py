import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def db(app):
    _db.session.begin_nested()
    yield _db
    _db.session.rollback()


@pytest.fixture(scope='function')
def token_comprador(app):
    return 'test-token-comprador'


@pytest.fixture(scope='function')
def token_productor(app):
    return 'test-token-productor'


@pytest.fixture(scope='function')
def token_agencia(app):
    return 'test-token-agencia'

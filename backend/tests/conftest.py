import pytest
import uuid
from app import create_app
from app.extensions import db as _db
from app.api.users.models import User
from flask_jwt_extended import create_access_token


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
    original_commit = _db.session.commit
    _db.session.commit = _db.session.flush
    yield _db
    _db.session.commit = original_commit
    _db.session.rollback()


@pytest.fixture(scope='function')
def comprador(db):
    user = User(
        id=str(uuid.uuid4()),
        name='Comprador Test',
        email='comprador@test.com',
        password='hashed_password',
        user_type='comprador',
    )
    db.session.add(user)
    db.session.flush()
    return user


@pytest.fixture(scope='function')
def productor(db):
    user = User(
        id=str(uuid.uuid4()),
        name='Productor Test',
        email='productor@test.com',
        password='hashed_password',
        user_type='productor',
    )
    db.session.add(user)
    db.session.flush()
    return user


@pytest.fixture(scope='function')
def agencia(db):
    user = User(
        id=str(uuid.uuid4()),
        name='Agencia Test',
        email='agencia@test.com',
        password='hashed_password',
        user_type='agencia',
    )
    db.session.add(user)
    db.session.flush()
    return user


@pytest.fixture(scope='function')
def token_comprador(comprador, app):
    with app.app_context():
        return create_access_token(
            identity=comprador.id,
            additional_claims={'user_type': comprador.user_type},
        )


@pytest.fixture(scope='function')
def token_productor(productor, app):
    with app.app_context():
        return create_access_token(
            identity=productor.id,
            additional_claims={'user_type': productor.user_type},
        )


@pytest.fixture(scope='function')
def token_agencia(agencia, app):
    with app.app_context():
        return create_access_token(
            identity=agencia.id,
            additional_claims={'user_type': agencia.user_type},
        )


@pytest.fixture(scope='function')
def auth_headers_comprador(token_comprador):
    return {'Authorization': f'Bearer {token_comprador}'}


@pytest.fixture(scope='function')
def auth_headers_productor(token_productor):
    return {'Authorization': f'Bearer {token_productor}'}


@pytest.fixture(scope='function')
def auth_headers_agencia(token_agencia):
    return {'Authorization': f'Bearer {token_agencia}'}

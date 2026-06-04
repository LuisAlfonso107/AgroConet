import json
import uuid
from flask_jwt_extended import create_access_token


class TestAuthMiddleware:

    def test_token_valido_inyecta_current_user(self, client, db, productor, app):
        with app.app_context():
            token = create_access_token(
                identity=productor.id,
                additional_claims={'user_type': productor.user_type},
            )
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/users/me', headers=headers)
        assert response.status_code == 200
        body = response.get_json()
        assert body['data']['email'] == productor.email

    def test_sin_token_retorna_401(self, client):
        response = client.get('/api/users/me')
        assert response.status_code == 401

    def test_token_invalido_retorna_401(self, client):
        headers = {'Authorization': 'Bearer invalidtoken123'}
        response = client.get('/api/users/me', headers=headers)
        assert response.status_code in (401, 422)

    def test_role_required_comprador(self, client, db, comprador, auth_headers_comprador, app):
        with app.app_context():
            token = create_access_token(
                identity=comprador.id,
                additional_claims={'user_type': comprador.user_type},
            )
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/users/me', headers=headers)
        assert response.status_code == 200

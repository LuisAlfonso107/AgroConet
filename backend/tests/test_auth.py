import json


class TestAuthRegister:

    def test_registro_exitoso(self, client, db):
        data = {
            'name': 'Nuevo Usuario',
            'email': 'nuevo@test.com',
            'password': 'password123',
            'user_type': 'productor',
        }
        response = client.post(
            '/api/auth/register',
            data=json.dumps(data),
            content_type='application/json',
        )
        assert response.status_code == 201
        body = response.get_json()
        assert body['data']['email'] == 'nuevo@test.com'
        assert body['data']['name'] == 'Nuevo Usuario'
        assert 'password' not in body['data']

    def test_email_duplicado(self, client, db, productor):
        data = {
            'name': 'Otro Usuario',
            'email': productor.email,
            'password': 'password123',
            'user_type': 'comprador',
        }
        response = client.post(
            '/api/auth/register',
            data=json.dumps(data),
            content_type='application/json',
        )
        assert response.status_code == 409
        body = response.get_json()
        assert 'error' in body

    def test_datos_invalidos(self, client, db):
        data = {
            'name': '',
            'email': 'invalido',
            'password': '12',
            'user_type': 'invalido',
        }
        response = client.post(
            '/api/auth/register',
            data=json.dumps(data),
            content_type='application/json',
        )
        assert response.status_code == 400


class TestAuthLogin:

    def test_login_exitoso(self, client, db):
        client.post(
            '/api/auth/register',
            data=json.dumps({
                'name': 'Login User',
                'email': 'login@test.com',
                'password': 'password123',
                'user_type': 'comprador',
            }),
            content_type='application/json',
        )
        response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'login@test.com', 'password': 'password123'}),
            content_type='application/json',
        )
        assert response.status_code == 200
        body = response.get_json()
        assert 'access_token' in body['data']
        assert 'refresh_token' in body['data']
        assert body['data']['user']['email'] == 'login@test.com'

    def test_login_credenciales_incorrectas(self, client, db):
        response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'noexiste@test.com', 'password': 'wrong'}),
            content_type='application/json',
        )
        assert response.status_code == 401
        body = response.get_json()
        assert 'Credenciales inválidas' in body['error']

    def test_login_datos_invalidos(self, client, db):
        response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'notanemail', 'password': ''}),
            content_type='application/json',
        )
        assert response.status_code == 400

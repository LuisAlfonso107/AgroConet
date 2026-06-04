import json
import uuid


class TestDashboard:

    def test_dashboard_comprador(self, client, db, comprador):
        from flask_jwt_extended import create_access_token
        token = create_access_token(
            identity=comprador.id,
            additional_claims={'user_type': comprador.user_type},
        )
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/dashboard/resumen', headers=headers)
        assert response.status_code == 200

    def test_dashboard_productor(self, client, db, productor):
        from flask_jwt_extended import create_access_token
        token = create_access_token(
            identity=productor.id,
            additional_claims={'user_type': productor.user_type},
        )
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/dashboard/resumen', headers=headers)
        assert response.status_code == 200

    def test_dashboard_agencia(self, client, db, agencia):
        from flask_jwt_extended import create_access_token
        token = create_access_token(
            identity=agencia.id,
            additional_claims={'user_type': agencia.user_type},
        )
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/dashboard/resumen', headers=headers)
        assert response.status_code == 200

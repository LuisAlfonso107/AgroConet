import json
import uuid


class TestTracking:

    def test_cambio_estado_valido_y_tracking(self, client, db, productor, comprador, agencia, app):
        with app.app_context():
            from flask_jwt_extended import create_access_token
            prod_token = create_access_token(
                identity=productor.id,
                additional_claims={'user_type': productor.user_type},
            )
            comp_token = create_access_token(
                identity=comprador.id,
                additional_claims={'user_type': comprador.user_type},
            )

        prod_resp = client.post(
            '/api/productos',
            data=json.dumps({
                'nombre': 'Café Tracking',
                'tipo': 'cafe',
                'precio': 200.0,
                'stock': 100,
                'humedad': 12.0,
                'variedad': 'Test',
                'region': 'Test',
                'pais': 'Honduras',
                'altura': '1200',
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {prod_token}'},
        )
        producto_id = prod_resp.get_json()['data']['id']

        pedido_resp = client.post(
            '/api/pedidos',
            data=json.dumps({
                'producto_id': producto_id,
                'nombre_producto': 'Café Tracking',
                'cantidad_quintales': 10,
                'precio_unitario': 200.0,
                'total': 2000.0,
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {comp_token}'},
        )
        pedido_id = pedido_resp.get_json()['data']['id']

        client.patch(
            f'/api/pedidos/{pedido_id}/estado',
            data=json.dumps({'estado': 'confirmado'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {comp_token}'},
        )
        client.patch(
            f'/api/pedidos/{pedido_id}/estado',
            data=json.dumps({'estado': 'en puerto'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {comp_token}'},
        )

        track_resp = client.get(
            f'/api/pedidos/{pedido_id}/tracking',
            headers={'Authorization': f'Bearer {comp_token}'},
        )
        assert track_resp.status_code == 200
        eventos = track_resp.get_json()['data']
        assert len(eventos) >= 3

    def test_transicion_estado_invalida(self, client, db, productor, comprador, app):
        with app.app_context():
            from flask_jwt_extended import create_access_token
            prod_token = create_access_token(
                identity=productor.id,
                additional_claims={'user_type': productor.user_type},
            )
            comp_token = create_access_token(
                identity=comprador.id,
                additional_claims={'user_type': comprador.user_type},
            )

        prod_resp = client.post(
            '/api/productos',
            data=json.dumps({
                'nombre': 'Café Trans',
                'tipo': 'cafe',
                'precio': 200.0,
                'stock': 100,
                'humedad': 12.0,
                'variedad': 'Test',
                'region': 'Test',
                'pais': 'Honduras',
                'altura': '1200',
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {prod_token}'},
        )
        producto_id = prod_resp.get_json()['data']['id']

        pedido_resp = client.post(
            '/api/pedidos',
            data=json.dumps({
                'producto_id': producto_id,
                'nombre_producto': 'Café Trans',
                'cantidad_quintales': 10,
                'precio_unitario': 200.0,
                'total': 2000.0,
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {comp_token}'},
        )
        pedido_id = pedido_resp.get_json()['data']['id']

        response = client.patch(
            f'/api/pedidos/{pedido_id}/estado',
            data=json.dumps({'estado': 'entregado'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {comp_token}'},
        )
        assert response.status_code == 422

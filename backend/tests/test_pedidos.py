import json
import uuid


class TestPedidos:

    def test_crear_pedido_exitoso(self, client, db, productor, comprador, app):
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

        prod_response = client.post(
            '/api/productos',
            data=json.dumps({
                'nombre': 'Café Venta',
                'tipo': 'cafe',
                'precio': 200.0,
                'stock': 50,
                'humedad': 12.0,
                'variedad': 'Test',
                'region': 'Test',
                'pais': 'Honduras',
                'altura': '1200',
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {prod_token}'},
        )
        producto_id = prod_response.get_json()['data']['id']

        data = {
            'producto_id': producto_id,
            'nombre_producto': 'Café Venta',
            'cantidad_quintales': 10,
            'precio_unitario': 200.0,
            'total': 2000.0,
        }
        response = client.post(
            '/api/pedidos',
            data=json.dumps(data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {comp_token}'},
        )
        assert response.status_code == 201
        body = response.get_json()
        assert body['data']['cantidad_quintales'] == 10

    def test_stock_insuficiente(self, client, db, productor, comprador, app):
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

        prod_response = client.post(
            '/api/productos',
            data=json.dumps({
                'nombre': 'Café Poco',
                'tipo': 'cafe',
                'precio': 200.0,
                'stock': 5,
                'humedad': 12.0,
                'variedad': 'Test',
                'region': 'Test',
                'pais': 'Honduras',
                'altura': '1200',
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {prod_token}'},
        )
        producto_id = prod_response.get_json()['data']['id']

        data = {
            'producto_id': producto_id,
            'nombre_producto': 'Café Poco',
            'cantidad_quintales': 50,
            'precio_unitario': 200.0,
            'total': 10000.0,
        }
        response = client.post(
            '/api/pedidos',
            data=json.dumps(data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {comp_token}'},
        )
        assert response.status_code == 422

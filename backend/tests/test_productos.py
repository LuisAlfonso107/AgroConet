import json
import uuid


class TestProductos:

    def test_crear_producto_exitoso(self, client, db, productor, auth_headers_productor):
        data = {
            'nombre': 'Café Caturra',
            'tipo': 'cafe',
            'precio': 150.0,
            'stock': 100,
            'humedad': 12.5,
            'variedad': 'Caturra',
            'region': 'Copán',
            'pais': 'Honduras',
            'altura': '1200',
        }
        response = client.post(
            '/api/productos',
            data=json.dumps(data),
            content_type='application/json',
            headers=auth_headers_productor,
        )
        assert response.status_code == 201
        body = response.get_json()
        assert body['data']['nombre'] == 'Café Caturra'
        assert body['data']['stock'] == 100
        assert body['data']['estado'] == 'disponible'
        assert 'id' in body['data']

    def test_crear_producto_stock_invalido(self, client, db, productor, auth_headers_productor):
        data = {
            'nombre': 'Café Test',
            'tipo': 'cafe',
            'precio': 100.0,
            'stock': 0,
            'humedad': 12.0,
            'variedad': 'Test',
            'region': 'Test',
            'pais': 'Honduras',
            'altura': '1000',
        }
        response = client.post(
            '/api/productos',
            data=json.dumps(data),
            content_type='application/json',
            headers=auth_headers_productor,
        )
        assert response.status_code == 422

    def test_crear_producto_usuario_no_productor(self, client, db, comprador, auth_headers_comprador):
        data = {
            'nombre': 'Café No Aut',
            'tipo': 'cafe',
            'precio': 100.0,
            'stock': 50,
            'humedad': 12.0,
            'variedad': 'Test',
            'region': 'Test',
            'pais': 'Honduras',
            'altura': '1000',
        }
        response = client.post(
            '/api/productos',
            data=json.dumps(data),
            content_type='application/json',
            headers=auth_headers_comprador,
        )
        assert response.status_code == 403

    def test_listar_productos_filtros(self, client, db, productor, auth_headers_productor):
        for i in range(3):
            client.post(
                '/api/productos',
                data=json.dumps({
                    'nombre': f'Café {i}',
                    'tipo': 'cafe',
                    'precio': 100 + i * 10,
                    'stock': 50 + i * 10,
                    'humedad': 12.0,
                    'variedad': 'Test',
                    'region': 'Copán',
                    'pais': 'Honduras',
                    'altura': '1200',
                }),
                content_type='application/json',
                headers=auth_headers_productor,
            )

        response = client.get('/api/productos?tipo=cafe')
        assert response.status_code == 200
        body = response.get_json()
        assert len(body['data']) >= 3
        assert 'meta' in body
        assert body['meta']['total'] >= 3

    def test_listar_productos_paginacion(self, client, db, productor, auth_headers_productor):
        for i in range(5):
            client.post(
                '/api/productos',
                data=json.dumps({
                    'nombre': f'Maíz {i}',
                    'tipo': 'maiz',
                    'precio': 80.0,
                    'stock': 200,
                    'humedad': 14.0,
                    'variedad': 'Test',
                    'region': 'Olancho',
                    'pais': 'Honduras',
                    'altura': '800',
                }),
                content_type='application/json',
                headers=auth_headers_productor,
            )
        response = client.get('/api/productos?page=1&limit=2')
        assert response.status_code == 200
        body = response.get_json()
        assert len(body['data']) <= 2
        assert body['meta']['page'] == 1
        assert body['meta']['limit'] == 2
        assert body['meta']['total'] >= 5

    def test_productos_sin_autenticacion(self, client, db):
        response = client.get('/api/productos')
        assert response.status_code == 200

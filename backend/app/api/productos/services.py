from app.extensions import db
from app.api.productos.models import Producto, ProductoEstado
from app.core.exceptions import NotFoundError, ForbiddenError, UnprocessableError
from app.core.pagination import paginate_query


class ProductoService:

    def listar(self, page=1, limit=20, filters=None):
        query = Producto.query

        if filters:
            if filters.get('tipo'):
                query = query.filter(Producto.tipo == filters['tipo'])
            if filters.get('precio_min'):
                query = query.filter(Producto.precio >= float(filters['precio_min']))
            if filters.get('precio_max'):
                query = query.filter(Producto.precio <= float(filters['precio_max']))
            if filters.get('region'):
                query = query.filter(Producto.region.ilike(f'%{filters["region"]}%'))
            if filters.get('pais'):
                query = query.filter(Producto.pais.ilike(f'%{filters["pais"]}%'))
            if filters.get('estado'):
                query = query.filter(Producto.estado == filters['estado'])
            if filters.get('certificaciones'):
                certs = filters['certificaciones'].split(',')
                query = query.filter(Producto.certificaciones.contains(certs))
            if filters.get('productor_id'):
                query = query.filter(Producto.productor_id == filters['productor_id'])

        query = query.order_by(Producto.created_at.desc())
        return paginate_query(query, page=page, limit=limit)

    def get_by_id(self, producto_id):
        producto = Producto.query.get(producto_id)
        if not producto:
            raise NotFoundError('Producto no encontrado')
        return producto

    def crear(self, data, productor_id):
        if data.get('stock', 0) <= 0:
            raise UnprocessableError('El stock debe ser mayor a 0')

        producto = Producto(
            nombre=data['nombre'],
            tipo=data['tipo'],
            precio=data['precio'],
            stock=data['stock'],
            estado=ProductoEstado.DISPONIBLE,
            productor_id=productor_id,
            humedad=data['humedad'],
            variedad=data['variedad'],
            region=data['region'],
            pais=data['pais'],
            altura=data['altura'],
            certificaciones=data.get('certificaciones', []),
            descripcion=data.get('descripcion'),
            imagen=data.get('imagen'),
            lat=data.get('lat'),
            lon=data.get('lon'),
        )
        db.session.add(producto)
        db.session.commit()
        return producto

    def actualizar(self, producto_id, data):
        producto = self.get_by_id(producto_id)
        if 'stock' in data and data['stock'] is not None and data['stock'] <= 0:
            raise UnprocessableError('El stock debe ser mayor a 0')

        allowed_fields = [
            'nombre', 'tipo', 'precio', 'stock', 'estado', 'humedad',
            'variedad', 'region', 'pais', 'altura', 'certificaciones',
            'descripcion', 'imagen', 'lat', 'lon',
        ]
        for field in allowed_fields:
            if field in data:
                setattr(producto, field, data[field])

        db.session.commit()
        return producto

    def eliminar(self, producto_id):
        producto = self.get_by_id(producto_id)
        db.session.delete(producto)
        db.session.commit()

import json
import os
from datetime import datetime
from app import create_app
from app.extensions import db, bcrypt
from app.api.users.models import User
from app.api.productos.models import Producto
from app.api.pedidos.models import Pedido
from app.api.tracking.models import TrackingEvento
from app.api.favoritos.models import Favorito

app = create_app('development')

def parse_date(date_str):
    if not date_str:
        return None
    # Remove 'Z' if present, replace T with space and parse
    date_str = date_str.replace('Z', '')
    if '.' in date_str:
        date_str = date_str.split('.')[0]
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None

with app.app_context():
    db_json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db.json'))
    print(f"Reading mock data from: {db_json_path}")
    
    if not os.path.exists(db_json_path):
        print("Error: db.json not found in the root directory!")
        exit(1)
        
    with open(db_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("Cleaning database...")
    TrackingEvento.query.delete()
    Pedido.query.delete()
    Favorito.query.delete()
    Producto.query.delete()
    User.query.delete()
    db.session.commit()

    print("Seeding users...")
    user_map = {}
    for u in data.get('users', []):
        raw_password = u['password']
        # Hash password so auth works with our bcrypt implementation
        password_hash = bcrypt.generate_password_hash(raw_password).decode('utf-8')
        
        user = User(
            id=str(u['id']),
            name=u['name'],
            email=u['email'].lower().strip(),
            password=password_hash,
            user_type=u['userType'],
            telefono=u.get('telefono'),
            empresa=u.get('empresa'),
            direccion_envio=u.get('direccionEnvio'),
            direcciones_envio=u.get('direccionesEnvio'),
            pais=u.get('pais'),
            preferencias_notificacion=u.get('preferenciasNotificacion'),
            finca=u.get('finca'),
            ubicacion=u.get('ubicacion'),
            descripcion=u.get('descripcion'),
            foto_perfil=u.get('fotoPerfil'),
            created_at=parse_date(u.get('createdAt'))
        )
        db.session.add(user)
        user_map[str(u['id'])] = user

    db.session.commit()
    print(f"Seeded {len(data.get('users', []))} users.")

    print("Seeding products...")
    product_map = {}
    for p in data.get('productos', []):
        prod = Producto(
            id=str(p['id']),
            nombre=p['nombre'],
            tipo=p['tipo'],
            precio=float(p['precio']),
            stock=int(p['stock']),
            estado=p.get('estado', 'disponible'),
            productor_id=str(p['productorId']),
            humedad=float(p.get('humedad', 0.0)),
            variedad=p.get('variedad', ''),
            region=p.get('region', ''),
            pais=p.get('pais', ''),
            altura=p.get('altura', ''),
            certificaciones=p.get('certificaciones', []),
            descripcion=p.get('descripcion'),
            imagen=p.get('imagen'),
            lat=p.get('lat'),
            lon=p.get('lon'),
            created_at=parse_date(p.get('createdAt'))
        )
        db.session.add(prod)
        product_map[str(p['id'])] = prod

    db.session.commit()
    print(f"Seeded {len(data.get('productos', []))} products.")

    print("Seeding favorites...")
    for fav in data.get('favoritos', []):
        f = Favorito(
            id=str(fav['id']),
            comprador_id=str(fav['compradorId']),
            producto_id=str(fav['productoId']),
            created_at=parse_date(fav.get('createdAt'))
        )
        db.session.add(f)
    
    db.session.commit()
    print(f"Seeded {len(data.get('favoritos', []))} favorites.")

    print("Seeding orders (pedidos)...")
    for ped in data.get('pedidos', []):
        prod_id = str(ped['productoId'])
        
        # Determine producer ID (fallback to product's producer if missing in order)
        prod_user_id = str(ped.get('productorId')) if ped.get('productorId') else None
        if not prod_user_id and prod_id in product_map:
            prod_user_id = product_map[prod_id].productor_id
        if not prod_user_id:
            prod_user_id = "2" # default producer if not found
            
        p = Pedido(
            id=str(ped['id']),
            producto_id=prod_id,
            comprador_id=str(ped['compradorId']),
            productor_id=prod_user_id,
            agencia_id="3" if ped.get('agenciaNombre') else None,  # Agencia Demo is "3"
            nombre_producto=ped['nombreProducto'],
            cantidad_quintales=float(ped['cantidadQuintales']),
            precio_unitario=float(ped['precioUnitario']),
            total=float(ped['total']),
            estado=ped.get('estado', 'solicitado').lower(),
            impuestos=float(ped.get('impuestos', 0.0)),
            created_at=parse_date(ped.get('createdAt'))
        )
        db.session.add(p)

    db.session.commit()
    print(f"Seeded {len(data.get('pedidos', []))} orders.")

    print("Seeding tracking events...")
    for tr in data.get('tracking', []):
        t = TrackingEvento(
            id=str(tr['id']),
            pedido_id=str(tr['pedidoId']),
            estado=tr['estado'].lower(),
            descripcion=tr['descripcion'],
            created_at=parse_date(tr.get('updatedAt'))
        )
        db.session.add(t)

    db.session.commit()
    print(f"Seeded {len(data.get('tracking', []))} tracking events.")
    print("Database seeding completed successfully!")

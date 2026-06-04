from sqlalchemy import func
from app.extensions import db
from app.api.pedidos.models import Pedido, PedidoEstado
from app.api.productos.models import Producto


class DashboardService:

    def resumen_comprador(self, usuario_id):
        pedidos = Pedido.query.filter_by(comprador_id=usuario_id).all()
        activos = [p for p in pedidos if p.estado in (
            PedidoEstado.SOLICITADO, PedidoEstado.CONFIRMADO,
            PedidoEstado.EN_PUERTO, PedidoEstado.EN_TRANSITO,
        )]
        total_invertido = sum(p.total for p in pedidos)
        return {
            'activos': len(activos),
            'entregados30': len([p for p in pedidos if p.estado == PedidoEstado.ENTREGADO]),
            'total_invertido': total_invertido,
        }

    def resumen_productor(self, usuario_id):
        pedidos = Pedido.query.filter_by(productor_id=usuario_id).all()
        pendientes = [p for p in pedidos if p.estado == PedidoEstado.SOLICITADO]
        confirmados = [p for p in pedidos if p.estado in (
            PedidoEstado.CONFIRMADO, PedidoEstado.EN_PUERTO,
            PedidoEstado.EN_TRANSITO, PedidoEstado.ENTREGADO,
        )]
        return {
            'pedidos_pendientes': len(pendientes),
            'total_vendido_qq': sum(p.cantidad_quintales for p in confirmados),
            'ingresos_estimados': sum(p.total for p in confirmados),
        }

    def resumen_agencia(self, usuario_id):
        todos = Pedido.query.all()
        activos = [p for p in todos if p.estado in (
            PedidoEstado.CONFIRMADO, PedidoEstado.EN_PUERTO, PedidoEstado.EN_TRANSITO,
        )]
        return {
            'total_pedidos': len(todos),
            'pedidos_activos': len(activos),
            'volumen_total': sum(p.cantidad_quintales for p in todos),
        }

class DashboardService:

    def resumen_comprador(self, usuario_id):
        """Get dashboard summary for a buyer.

        Args:
            usuario_id (str): UUID of the buyer.

        Returns:
            dict: Summary with activos, entregados30, total_invertido.
        """
        raise NotImplementedError

    def resumen_productor(self, usuario_id):
        """Get dashboard summary for a producer.

        Args:
            usuario_id (str): UUID of the producer.

        Returns:
            dict: Summary with pedidos_pendientes, total_vendido_qq, ingresos_estimados.
        """
        raise NotImplementedError

    def resumen_agencia(self, usuario_id):
        """Get dashboard summary for an agency.

        Args:
            usuario_id (str): UUID of the agency.

        Returns:
            dict: Summary with total_pedidos, pedidos_activos, volumen_total.
        """
        raise NotImplementedError

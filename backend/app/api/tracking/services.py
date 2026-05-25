class TrackingService:

    def listar_por_pedido(self, pedido_id, order='asc'):
        """List tracking events for an order.

        Args:
            pedido_id (str): UUID of the order.
            order (str): Sort order ('asc' or 'desc').

        Returns:
            list: List of TrackingEvento instances.

        Raises:
            NotFoundError: If order does not exist.
        """
        raise NotImplementedError

    def agregar_evento(self, pedido_id, user_id, data):
        """Add a new tracking event to an order.

        Args:
            pedido_id (str): UUID of the order.
            user_id (str): UUID of the user adding the event.
            data (dict): Validated event data with estado and descripcion.

        Returns:
            TrackingEvento: Created event instance.

        Raises:
            NotFoundError: If order does not exist.
            UnprocessableError: If state transition is invalid.
        """
        raise NotImplementedError

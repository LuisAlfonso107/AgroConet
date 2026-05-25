class PedidoService:

    def listar(self, page=1, limit=20, user_id=None, user_type=None):
        """List orders with pagination, filtered by user role.

        Args:
            page (int): Page number.
            limit (int): Items per page.
            user_id (str, optional): Filter by user ID.
            user_type (str, optional): User role to determine filter field.

        Returns:
            dict: Paginated response with 'data' and 'meta' keys.
        """
        raise NotImplementedError

    def get_by_id(self, pedido_id):
        """Get a single order by ID.

        Args:
            pedido_id (str): UUID of the order.

        Returns:
            Pedido: Order instance with relaciones.

        Raises:
            NotFoundError: If order does not exist.
        """
        raise NotImplementedError

    def crear_pedido(self, data, comprador_id):
        """Create a new order.

        Args:
            data (dict): Validated order data.
            comprador_id (str): UUID of the buyer.

        Returns:
            Pedido: Created order instance.

        Raises:
            NotFoundError: If product does not exist.
        """
        raise NotImplementedError

    def cambiar_estado(self, pedido_id, nuevo_estado):
        """Update order status.

        Args:
            pedido_id (str): UUID of the order.
            nuevo_estado (str): New state value.

        Returns:
            Pedido: Updated order instance.

        Raises:
            NotFoundError: If order does not exist.
            UnprocessableError: If state transition is invalid.
        """
        raise NotImplementedError

    def cancelar(self, pedido_id):
        """Cancel an order.

        Args:
            pedido_id (str): UUID of the order.

        Returns:
            dict: Success message.

        Raises:
            NotFoundError: If order does not exist.
            UnprocessableError: If order cannot be cancelled.
        """
        raise NotImplementedError

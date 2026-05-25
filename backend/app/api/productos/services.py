class ProductoService:

    def listar(self, page=1, limit=20, filters=None):
        """List products with pagination and optional filters.

        Args:
            page (int): Page number.
            limit (int): Items per page.
            filters (dict, optional): Filter by tipo, estado, region, pais.

        Returns:
            dict: Paginated response with 'data' and 'meta' keys.
        """
        raise NotImplementedError

    def get_by_id(self, producto_id):
        """Get a single product by ID.

        Args:
            producto_id (str): UUID of the product.

        Returns:
            Producto: Product instance.

        Raises:
            NotFoundError: If product does not exist.
        """
        raise NotImplementedError

    def crear(self, data, productor_id):
        """Create a new product.

        Args:
            data (dict): Validated product data.
            productor_id (str): UUID of the creator user.

        Returns:
            Producto: Created product instance.

        Raises:
            UnprocessableError: If validation fails.
        """
        raise NotImplementedError

    def actualizar(self, producto_id, data):
        """Update an existing product.

        Args:
            producto_id (str): UUID of the product.
            data (dict): Validated subset of fields to update.

        Returns:
            Producto: Updated product instance.

        Raises:
            NotFoundError: If product does not exist.
            ForbiddenError: If user is not the owner.
        """
        raise NotImplementedError

    def eliminar(self, producto_id):
        """Delete a product.

        Args:
            producto_id (str): UUID of the product.

        Raises:
            NotFoundError: If product does not exist.
            ForbiddenError: If user is not the owner.
        """
        raise NotImplementedError

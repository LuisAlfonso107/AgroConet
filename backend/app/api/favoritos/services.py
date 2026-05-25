class FavoritoService:

    def listar(self, comprador_id):
        """List favorites for a buyer.

        Args:
            comprador_id (str): UUID of the buyer.

        Returns:
            list: List of Favorito instances with nested producto.
        """
        raise NotImplementedError

    def agregar(self, comprador_id, producto_id):
        """Add a product to favorites.

        Args:
            comprador_id (str): UUID of the buyer.
            producto_id (str): UUID of the product.

        Returns:
            Favorito: Created favorite instance.

        Raises:
            ConflictError: If already favorited.
            NotFoundError: If product does not exist.
        """
        raise NotImplementedError

    def eliminar(self, favorito_id):
        """Remove a favorite.

        Args:
            favorito_id (str): UUID of the favorite entry.

        Raises:
            NotFoundError: If favorite does not exist.
        """
        raise NotImplementedError

class ContactoService:

    def listar(self, usuario_id=None):
        """List contact inquiries, optionally filtered by user.

        Args:
            usuario_id (str, optional): UUID of the user.

        Returns:
            list: List of Contacto instances.
        """
        raise NotImplementedError

    def crear(self, data, usuario_id):
        """Create a contact inquiry from a user about a product.

        Args:
            data (dict): Validated contact data.
            usuario_id (str): UUID of the sender.

        Returns:
            Contacto: Created contact instance.

        Raises:
            NotFoundError: If product does not exist.
        """
        raise NotImplementedError

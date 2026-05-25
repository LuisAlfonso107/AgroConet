class MensajeService:

    def crear(self, data):
        """Create a contact message from an anonymous visitor.

        Args:
            data (dict): Validated message data with nombre, email, asunto, mensaje.

        Returns:
            MensajeContacto: Created message instance.

        Raises:
            UnprocessableError: If validation fails.
        """
        raise NotImplementedError

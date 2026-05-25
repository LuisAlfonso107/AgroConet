class NotificacionService:

    def listar(self, usuario_id):
        """List notifications for a user.

        Args:
            usuario_id (str): UUID of the user.

        Returns:
            list: List of Notificacion instances.
        """
        raise NotImplementedError

    def marcar_leida(self, notificacion_id):
        """Mark a notification as read.

        Args:
            notificacion_id (str): UUID of the notification.

        Returns:
            Notificacion: Updated notification instance.

        Raises:
            NotFoundError: If notification does not exist.
        """
        raise NotImplementedError

class UserService:

    def get_me(self, user_id):
        """Get current authenticated user profile.

        Args:
            user_id (str): UUID of the authenticated user.

        Returns:
            User: User instance with all profile fields.

        Raises:
            NotFoundError: If user does not exist.
        """
        raise NotImplementedError

    def update_me(self, user_id, data):
        """Update current user profile fields.

        Args:
            user_id (str): UUID of the authenticated user.
            data (dict): Validated subset of profile fields to update.

        Returns:
            User: Updated user instance.

        Raises:
            NotFoundError: If user does not exist.
        """
        raise NotImplementedError

    def change_password(self, user_id, current_password, new_password):
        """Change user password after verifying current password.

        Args:
            user_id (str): UUID of the authenticated user.
            current_password (str): Current plain-text password.
            new_password (str): New plain-text password.

        Returns:
            dict: Success message.

        Raises:
            UnauthorizedError: If current_password does not match.
            UnprocessableError: If new_password does not meet requirements.
        """
        raise NotImplementedError

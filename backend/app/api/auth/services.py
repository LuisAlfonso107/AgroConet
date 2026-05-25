class AuthService:

    def register(self, data):
        """Register a new user.

        Args:
            data (dict): Validated registration data with name, email, password, user_type.

        Returns:
            dict: Created user data.

        Raises:
            ConflictError: If email already exists.
            UnprocessableError: If validation fails.
        """
        raise NotImplementedError

    def login(self, data):
        """Authenticate user and return tokens.

        Args:
            data (dict): Validated login data with email and password.

        Returns:
            dict: Access token, refresh token, and user data.

        Raises:
            UnauthorizedError: If credentials are invalid.
        """
        raise NotImplementedError

    def refresh_token(self, identity):
        """Generate a new access token using refresh token.

        Args:
            identity (str): User ID from JWT identity.

        Returns:
            dict: New access token.

        Raises:
            UnauthorizedError: If refresh token is invalid or expired.
        """
        raise NotImplementedError

    def logout(self, identity):
        """Invalidate refresh token for a user.

        Args:
            identity (str): User ID.

        Returns:
            dict: Success message.
        """
        raise NotImplementedError

class NotFoundError(Exception):
    def __init__(self, message='Recurso no encontrado'):
        self.message = message
        super().__init__(self.message)


class ForbiddenError(Exception):
    def __init__(self, message='No tienes permisos para realizar esta accion'):
        self.message = message
        super().__init__(self.message)


class ConflictError(Exception):
    def __init__(self, message='El recurso ya existe'):
        self.message = message
        super().__init__(self.message)


class UnprocessableError(Exception):
    def __init__(self, message='Datos de entrada invalidos'):
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(Exception):
    def __init__(self, message='Token no proporcionado o invalido'):
        self.message = message
        super().__init__(self.message)

from .exceptions import (
    NotFoundError,
    ForbiddenError,
    ConflictError,
    UnprocessableError,
    UnauthorizedError,
)
from .responses import error_response


def register_error_handlers(app):

    @app.errorhandler(NotFoundError)
    def handle_not_found(error):
        return error_response(error.message, 404)

    @app.errorhandler(ForbiddenError)
    def handle_forbidden(error):
        return error_response(error.message, 403)

    @app.errorhandler(ConflictError)
    def handle_conflict(error):
        return error_response(error.message, 409)

    @app.errorhandler(UnprocessableError)
    def handle_unprocessable(error):
        return error_response(error.message, 422)

    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized(error):
        return error_response(error.message, 401)

    @app.errorhandler(404)
    def handle_404(error):
        return error_response('Recurso no encontrado', 404)

    @app.errorhandler(500)
    def handle_500(error):
        return error_response('Error interno del servidor', 500)

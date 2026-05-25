from flask import g
from app.core.responses import success_response, error_response
from app.api.dashboard.services import DashboardService

dashboard_service = DashboardService()


def resumen():
    user_type = g.get('current_user_type')
    user_id = g.current_user_id

    if user_type == 'comprador':
        result = dashboard_service.resumen_comprador(user_id)
    elif user_type == 'productor':
        result = dashboard_service.resumen_productor(user_id)
    elif user_type == 'agencia':
        result = dashboard_service.resumen_agencia(user_id)
    else:
        return error_response('Tipo de usuario no valido', 400)

    return success_response(result)

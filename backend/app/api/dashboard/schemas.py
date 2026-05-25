from marshmallow import fields
from app.extensions import ma


class ResumenCompradorSchema(ma.Schema):
    activos = fields.Integer()
    entregados30 = fields.Integer()
    total_invertido = fields.Float()


class ResumenProductorSchema(ma.Schema):
    pedidos_pendientes = fields.Integer()
    total_vendido_qq = fields.Float()
    ingresos_estimados = fields.Float()


class ResumenAgenciaSchema(ma.Schema):
    total_pedidos = fields.Integer()
    pedidos_activos = fields.Integer()
    volumen_total = fields.Float()

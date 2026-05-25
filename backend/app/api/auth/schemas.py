from marshmallow import fields, validate
from app.extensions import ma


class RegisterSchema(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    user_type = fields.String(required=True, validate=validate.OneOf(['comprador', 'productor', 'agencia']))


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class TokenResponseSchema(ma.Schema):
    access_token = fields.String()
    refresh_token = fields.String()
    user = fields.Dict()

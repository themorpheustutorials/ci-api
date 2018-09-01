from marshmallow import Schema, fields, validate


class DaoCreateChallengeSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    flag = fields.Str(required=True)
    category = fields.Str(required=True)
    urls = fields.List(fields.Dict(), required=True)


class DaoUrlSchema(Schema):
    description = fields.Str(required=True)
    url = fields.Str(required=True)


class DaoUpdateChallengeSchema(Schema):
    description = fields.Str(validate=[validate.Length(min=1, max=512)])
    url = fields.Str(validate=[validate.Length(min=1, max=10)])
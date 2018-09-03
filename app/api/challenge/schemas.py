from marshmallow import Schema, fields, validate


class DaoCreateChallengeSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    flag = fields.Str(required=True)
    category = fields.Str(required=True)
    urls = fields.List(fields.Dict()) or []


class DaoUrlSchema(Schema):
    description = fields.Str(required=True)
    url = fields.Str(required=True)


class DaoUpdateChallengeSchema(Schema):
    description = fields.Str(validate=[validate.Length(min=1, max=512)])
    url = fields.Str()
    yt_challenge_id = fields.Str(load_from='ytChallengeId', validate=[validate.Length(min=0, max=20)])
    yt_solution_id = fields.Str(load_from='ytSolutionId', validate=[validate.Length(min=0, max=20)])

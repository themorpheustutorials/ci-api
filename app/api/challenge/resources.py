from flask.views import MethodView
from flask import request

from ..schemas import ResultSchema, ResultErrorSchema
from .models import Challenge
from ..categories import Category
from app.db import db
from ..authentication import require_token, require_admin
from .schemas import DaoCreateChallengeSchema, DaoUpdateChallengeSchema
from ..solve import Solve


class ChallengeResource(MethodView):
    """
    curl -H "Access-Token: $token" -X GET localhost:5000/api/challenge
    curl -H "Access-Token: $token" -X GET localhost:5000/api/challenge/test
    """
    @require_token
    def get(self, _id, **_):
        if _id is None:
            # get all challenges
            return ResultSchema(
                data=[d.jsonify() for d in Challenge.query.all()]
            ).jsonify()
        else:
            # get the challenge object by the submitted name in the resource (url)
            challenge = Challenge.query.filter_by(id=_id).first()
            if not challenge:
                return ResultErrorSchema(
                    message='Challenge does not exist!',
                    errors=['challenge does not exist']
                ).jsonify()
            data = challenge.jsonify()
            challenge_solves = Solve.query.filter_by(challenge=challenge).first()
            if challenge_solves:
                print(challenge_solves.jsonify())
            data['solved'] = True
            return ResultSchema(
                data=data
            ).jsonify()

    """
    Create a new challenge
    curl -H "Access-Token: $token" -X POST localhost:5000/api/challenge -H "Content-Type: application/json" \
    -d '{"name": "Test", "description": "TestChallenge", "flag": "TMT{t3$T}", "category": "HC"}'
    """
    @require_token
    @require_admin
    def post(self, **_):
        data = request.get_json() or {}
        schema = DaoCreateChallengeSchema()
        # use the schema to validate the submitted data
        error = schema.validate(data)
        if error:
            return ResultErrorSchema(
                message='Payload is invalid',
                errors=error,
                status_code=400
            ).jsonify()
        # check if the flag for the challenge in already in use
        for challenge in Challenge.query.all():
            if data.get('flag') == challenge.flag:
                return ResultErrorSchema(
                    message='Flag already in use!',
                    errors=['flag already in use'],
                    status_code=400
                ).jsonify()
        category = Category.query.filter_by(name=data.get('category')).first()
        # create the challenge
        challenge = Challenge(
            name=data.get('name'),
            description=data.get('description'),
            flag=data.get('flag'),
            category=category,
            yt_challenge_id=data.get('ytChallengeId') or None,
            yt_solution_id=data.get('ytSolutionId') or None
        )

        # add the challenge object to the database
        db.session.add(challenge)
        # commit db changes (urls + challenge)
        db.session.commit()
        return ResultSchema(
            data=challenge.jsonify(),
            status_code=201
        ).jsonify()

    """
    curl -H "Access-Token: $token" -X PUT localhost:5000/api/challenge/test -H "Content-Type: application/json" \
    -d '{"description": "a"}'
    """
    @require_token
    @require_admin
    def put(self, _id, **_):
        data = request.get_json() or {}
        schema = DaoUpdateChallengeSchema()
        # use the schema to validate the submitted data
        data, error = schema.load(data)
        if error:
            return ResultErrorSchema(
                message='Payload is invalid',
                errors=error,
                status_code=400
            ).jsonify()
        # get the challenge object by the submitted name
        challenge = Challenge.query.filter_by(id=_id).first()
        if not challenge:
            return ResultErrorSchema(
                message='Challenge does not exist!',
                errors=['Challenge does not exist'],
                status_code=404
            ).jsonify()
        for key, val in data.items():
            # set the submitted values for the submitted key's
            setattr(challenge, key, val)
        # save the changes
        db.session.commit()
        return ResultSchema(
            data=challenge.jsonify()
        ).jsonify()

import os
from flask import Flask, send_from_directory

from .api import UserResource, AuthResource, RoleResource, ChallengeResource, SolveResource, CategoryResource
from .config import ProductionConfig, DevelopmentConfig
from .db import db
from .views import general, challenges, admin


def create_app(testing_config=None):
    # create flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # check which config should be used, can be defined in the environment variable FLASK_ENV
    env = os.environ.get('FLASK_ENV')
    # load config

    if testing_config is None:
        if env == 'development':
            app.config.from_object(DevelopmentConfig)
        else:
            app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(testing_config)

    db.init_app(app)
    register_models()
    with app.app_context():
        # create all tables in the database
        db.create_all()
    register_views(app)
    register_resource(app, UserResource, 'user_api', '/api/users', pk='uuid', pk_type='string')
    register_resource(app, AuthResource, 'auth_api', '/api/auth', pk=None, get=False, put=False)
    register_resource(app, RoleResource, 'role_api', '/api/roles', pk='name', pk_type='string')
    register_resource(app, ChallengeResource, 'challenge_api', '/api/challenges', delete=False)
    register_resource(app, SolveResource, 'solve_api', '/api/solve', get=False, delete=False)
    register_resource(app, CategoryResource, 'category_api', '/api/categories', pk='name', pk_type='string')

    return app


def register_models():
    # noinspection PyUnresolvedReferences
    from .api import User, Token, Role, Challenge, Solve, Url, Category


def register_resource(app, resource, endpoint, url, pk='_id', pk_type='int',
                      get=True, get_all=True, post=True, put=True, delete=True):
    view_func = resource.as_view(endpoint)
    if get_all:
        app.add_url_rule(url, defaults={pk: None} if get else None, view_func=view_func, methods=['GET'])
    if post:
        app.add_url_rule(url, view_func=view_func, methods=['POST'])
    if get:
        app.add_url_rule(f'{url}/<{pk_type}:{pk}>', view_func=view_func, methods=['GET'])
    if put:
        app.add_url_rule(f'{url}/<{pk_type}:{pk}>', view_func=view_func, methods=['PUT'])
    if delete:
        app.add_url_rule(f'{url}/<{pk_type}:{pk}>' if pk else url, view_func=view_func, methods=['DELETE'])


def register_views(app):
    # register blueprints
    app.register_blueprint(general)
    app.register_blueprint(challenges, url_prefix='/challenges')
    app.register_blueprint(admin, url_prefix='/admin')

    # 404 error page
    @app.errorhandler(404)
    def not_found(e):
        return 'File not found!', 404

    # 403 error page
    @app.errorhandler(403)
    def permission_denied(e):
        return 'Permissions Denied!', 403

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(general.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon'
        )

    @app.route('/robots.txt')
    def robots():
        return send_from_directory(os.path.join(general.root_path, 'static'), 'robots.txt', mimetype='text/plain')

    @app.route('/static/vendor/images/sort_both.png')
    def sort_both():
        return send_from_directory(
            os.path.join(general.root_path, 'static/vendor/datatables/images/'), 'sort_both.png', mimetype='image/png'
        )

    @app.route('/static/vendor/images/sort_asc.png')
    def sort_asc():
        return send_from_directory(
            os.path.join(general.root_path, 'static/vendor/datatables/images/'), 'sort_asc.png', mimetype='image/png'
        )

    @app.route('/static/vendor/images/sort_desc.png')
    def sort_desc():
        return send_from_directory(
            os.path.join(general.root_path, 'static/vendor/datatables/images/'), 'sort_desc.png', mimetype='image/png'
        )

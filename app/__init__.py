from .app import Flask
from app.models.mongo import mongo
from app.settings import get_args


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugin(app):
    mongo.init_app(app)


def create_app():
    flask_app = Flask(__name__)
    args = get_args()
    flask_app.config.from_object(args)
    register_blueprints(flask_app)
    register_plugin(flask_app)

    return flask_app

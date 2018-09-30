from .app import Flask
from app.models.mongo import mongo


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugin(app):
    mongo.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.setting")
    register_blueprints(app)
    register_plugin(app)

    return app

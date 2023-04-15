from flask import Flask
from flask_cors import CORS


def init_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    with app.app_context():
        from src.endpoints.github import github_api

        app.register_blueprint(github_api)

    return app

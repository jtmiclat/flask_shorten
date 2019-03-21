import os
from flask import Flask
from .models import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI"
    )
    app.config["OPENAPI_VERSION"] = "3.0.2"
    db.init_app(app)
    from .views import UrlMapping, Redirection, api, url_bp

    api.init_app(app)
    api.register_blueprint(url_bp)
    app.add_url_rule(
        "/<path:path>", view_func=Redirection.as_view("redirection")
    )
    return app

import os
import logging

from flask import Flask

from .models import db

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

logger = logging.getLogger(__name__)


def set_config(app, testing=False):
    """Set up config

    UsTODO: Move this to an config class
    """
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_database = os.getenv("POSTGRES_DATABASE")
    postgres_service = os.getenv("POSTGRES_SERVICE")
    if (
        postgres_password is not None
        and postgres_password is not None
        and postgres_service is not None
        and postgres_user is not None
    ):
        uri = (
            "postgresql+psycopg2://"
            + postgres_user
            + ":"
            + postgres_password
            + "@"
            + postgres_service
            + "/"
            + postgres_database
        )
    else:
        uri = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite://")
        logger.warning("Missing postgres info using %s", uri)

    app.config["TESTING"] = testing
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/doc"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.19.5/"


def create_app(testing=False):
    """Create app """
    sentry_dsn = os.getenv("SENTRU_DSN")
    if sentry_dsn is not None:
        sentry_sdk.init(dsn=sentry_dsn, integrations=[FlaskIntegration()])
        logger.info("Using sentry monitoring")
    else:
        logger.warning("Found no sentry_dsn. Not using sentry")
    app = Flask(__name__)
    set_config(app, testing)
    db.init_app(app)
    from .views import Redirection, HomePage, api, url_bp

    api.init_app(app)
    api.register_blueprint(url_bp)
    app.add_url_rule("/<path:path>", view_func=Redirection.as_view("redirection"))
    app.add_url_rule("/", view_func=HomePage.as_view("HomePage"))
    return app

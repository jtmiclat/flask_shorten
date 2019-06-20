import os
import logging

from flask import Flask
from .models import db

logger = logging.getLogger(__name__)

def set_config(app):
    """Set up config

    TODO: Move this to an config class 
    """
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_database = os.getenv("POSTGRES_DATABASE")
    postgres_service = os.getenv("POSTGRES_SERVICE")
    if postgres_password and postgres_password and postgres_service and postgres_user:
        uri = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_service}/{postgres_database}"
    else:
        logger.warning("Missing postgres info using passing None")
        uri = None

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/doc"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.19.5/"
    )



def create_app():
    """Create app """
    app = Flask(__name__)
    db.init_app(app)
    set_config(app)
    from .views import UrlMapping, Redirection, HomePage, api, url_bp

    api.init_app(app)
    api.register_blueprint(url_bp)
    app.add_url_rule(
        "/<path:path>", view_func=Redirection.as_view("redirection")
    )
    app.add_url_rule(
        "/", view_func=HomePage.as_view("HomePage")
    )
    return app

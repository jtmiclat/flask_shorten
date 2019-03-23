import os
from flask import Flask
from .models import db

def set_config(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI"
    )
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/doc"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.19.5/"
    )



def create_app():
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

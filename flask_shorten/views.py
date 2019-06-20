from flask.views import MethodView
from flask import request, redirect, send_from_directory
from sqlalchemy import func
from marshmallow import Schema, fields, validate
from flask_rest_api import Api, Blueprint, abort

api = Api()

from .models import UrlMapper, db

url_bp = Blueprint("url", "url", url_prefix="/url", description="Url Mapping Api")


@api.definition("UrlMappingRequest")
class UrlMappingRequest(Schema):
    """Schema for generating of url mapping"""

    class Meta:
        strict = True

    url = fields.Url(required=True)
    custom_path = fields.String(
        required=False,
        validate=[
            validate.Length(min=6, max=88),
            validate.Regexp(
                r"[a-zA-Z0-9]*$", error="Can only contain alphanumeric characters"
            ),
        ],
    )


@api.definition("UrlMappingResponse")
class UrlMappingResponse(Schema):
    """Schema for response of url mapping"""

    class Meta:
        strict = True

    url = fields.Url(required=True)
    path = fields.String(required=False)


@api.definition("UrlMappingQuery")
class UrlMappingQuery(Schema):
    """Schema for querying url mappings."""

    class Meta:
        strict = True

    path = fields.String(required=True)


def create_url_mapper(url: str, path: str = None) -> UrlMapper:
    """Creates a new url based on path.
    
    If path is none, generates random hash. 
    Raises an abort if path already exists in database
    """
    custom = True
    if not path:
        custom = False
        path = UrlMapper.generate_hash_path()

    url_mapper = UrlMapper.query.filter_by(path=path).one_or_none()
    if url_mapper is not None:
        abort(409, message="That path is already taken in use")
    url_mapper = UrlMapper(url=url, path=path, custom=custom)
    db.session.add(url_mapper)
    db.session.commit()
    return url_mapper


@url_bp.route("/")
class UrlMapping(MethodView):
    """Resource for generating new url endpoints"""

    @url_bp.arguments(UrlMappingQuery, location="query")
    @url_bp.response(UrlMappingResponse)
    def get(self, args):
        path = args.get("path")
        return UrlMapper.query.filter_by(path=path).one_or_none()

    @url_bp.arguments(UrlMappingRequest)
    @url_bp.response(UrlMappingResponse)
    def post(self, args):
        url = args.get("url")
        path = args.get("custom_path")
        url_mapper = create_url_mapper(url, path)
        return url_mapper


class Redirection(MethodView):
    """Redirect to appropriate endpoint.

    TODO:
    - Record incoming headers and cookies then store them in a database
    """

    def get(self, path):
        result = UrlMapper.query.filter_by(path=path).one_or_none()
        if result is None:
            abort(404, message="No url found for path %s" % path)
        return redirect(result.url)


class HomePage(MethodView):
    """Deploy homepage html"""

    def get(self):
        return send_from_directory("static", "homepage.html")

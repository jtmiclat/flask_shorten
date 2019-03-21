from flask.views import MethodView
from flask import request, jsonify, redirect
from sqlalchemy import func
from marshmallow import Schema, fields, validate
from flask_rest_api import Api, Blueprint, abort

api = Api()

from .models import UrlMapper, db

url_bp = Blueprint("url", "url", url_prefix="/url", description="???")


@api.definition("UrlMappingRequest")
class UrlMappingRequest(Schema):
    class Meta:
        strict = True

    url = fields.Url(required=True)
    custom_path = fields.String(
        required=False,
        validate=[
            validate.Length(min=6, max=88),
            validate.Regexp(
                r"[a-zA-Z0-9]*$",
                error="Can only contain alphanumeric characters",
            ),
        ],
    )


@api.definition("UrlMappingResponse")
class UrlMappingResponse(Schema):
    class Meta:
        strict = True

    url = fields.Url(required=True)
    path = fields.String(required=False)


@api.definition("UrlMappingQuery")
class UrlMappingQuery(Schema):
    class Meta:
        strict = True

    path = fields.String(required=True)


def create_url_mapper(url, path=None):
    # Make sure no duplicates
    custom = True
    if not path:
        custom = False
        path = UrlMapper.generate_hash_path()

    url_mapper = UrlMapper.query.filter_by(path=path).one_or_none()
    if url_mapper is not None:
        abort(409, message="That path is already taken in use" )
    url_mapper = UrlMapper(url=url, path=path, custom=custom)
    db.session.add(url_mapper)
    db.session.commit()
    return url_mapper


@url_bp.route("/")
class UrlMapping(MethodView):
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
    def get(self, path):
        result = UrlMapper.query.filter_by(path=path).one_or_none()
        if result is None:
            abort(404, message="No url found for path %s" % path)
        return redirect(result.url)

class HealthCheck(MethodView):
    def get(self):
        return "Health Check of flask shorten"
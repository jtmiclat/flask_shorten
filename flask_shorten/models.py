from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from shortuuid import ShortUUID

HASH_LENGTH = 8

db = SQLAlchemy()


class UrlMapper(db.Model):  # type: ignore
    """URL Mapper"""

    __tablename__ = "url_mapper"
    id = db.Column("id", db.Integer, primary_key=True)
    url = db.Column("url", db.String, nullable=False)
    path = db.Column("path", db.String, unique=True)
    custom = db.Column("custom", db.Boolean, nullable=False)
    created_on = db.Column(
        "created_on", db.DateTime, nullable=False, default=datetime.utcnow
    )

    @staticmethod
    def generate_hash_path():
        """Generates a hash ussing UUID

        WARNING: There is a chance that hash will be repeated especially since
        UUID is only 8 characters long
        """
        return ShortUUID().random(HASH_LENGTH)


# TODO: Table for Url Uses
# class UrlUse(db.Model):
#     id = db.Column("id", db.Integer, primary_key=True)
#     cookies = db.Column("cookies", db.String)
#     headers = db.Column("headers", db.JSON)
#     timestamp = db.Column(
#         "created_on", db.DateTime, nullable=False, default=datetime.utcnow
#     )

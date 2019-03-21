from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from shortuuid import ShortUUID

HASH_LENGTH = 8

db = SQLAlchemy()


class UrlMapper(db.Model):
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
        return ShortUUID().random(HASH_LENGTH)


"""
class UrlUses(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    cookies = db.Column("cookies", db.String)
    headers = db.Column("headers", db.JSON)
    timestamp = db.Column(
        "created_on", db.DateTime, nullable=False, default=datetime.utcnow
    )
"""

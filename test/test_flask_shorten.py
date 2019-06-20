import os
import pytest

from flask_shorten import create_app
from flask_shorten.models import db, UrlMapper


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")
    app = create_app(testing=True)
    yield app


@pytest.fixture
def database(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


def test_custom_path_creation(app, database):
    client = app.test_client()
    client.post(
        "/url/",
        json={"url": "http://localhost.dev", "custom_path": "localhost"},
    )
    a = client.get("/localhost")
    assert a.status_code == 302
    assert a.location == "http://localhost.dev"


def test_random_path_creation(database, app, monkeypatch):
    client = app.test_client()
    monkeypatch.setattr(
        UrlMapper, "generate_hash_path", lambda: "randomstring"
    )
    client.post("/url/", json={"url": "http://localhosting.dev"})
    a = client.get("/randomstring")
    assert a.status_code == 302
    assert a.location == "http://localhosting.dev"


def test_taken_path(app, database, monkeypatch):
    client = app.test_client()
    client.post(
        "/url/",
        json={"url": "http://localhost.dev", "custom_path": "localhost"},
    )
    a = client.post(
        "/url/",
        json={"url": "http://localhost.dev", "custom_path": "localhost"},
    )
    assert a.status_code == 409


def test_no_path(app, database, monkeypatch):
    client = app.test_client()
    a = client.get("notexisting")
    assert a.status_code == 404

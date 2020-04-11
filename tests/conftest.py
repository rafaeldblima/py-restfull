import pytest

from api.api import API


@pytest.fixture
def app():
    return API(templates_dir="tests/templates", debug=False)


@pytest.fixture
def client(app):
    return app.session()

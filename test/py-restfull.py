from pytest import fixture, raises
from requests import Session

from api import API


@fixture
def api():
    return API()


@fixture
def client(api) -> Session:
    return api.test_session()


def test_basic_route(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"


def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with raises(AssertionError):
        @api.route("/home")
        def home2(req, resp):
            resp.text = "YOLO"


def test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "TEXT_RESPONSE"

    @api.route("/test")
    def test(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get("http://testserver/test").text == RESPONSE_TEXT


def test_parametrized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hello {name}"

    assert client.get("http://testserver/rafael").text == "hello rafael"
    assert client.get("http://testserver/brasil").text == "hello brasil"


def test_class_handler_requests(api, client):
    GET_RESP = "Books Page"
    POST_RESP = "Endpoint to create a book"
    DELETE_RESP = "Endpoint to delete a book"

    @api.route("/book")
    class BooksHandler:
        def get(self, req, resp):
            resp.text = GET_RESP

        def post(self, req, resp):
            resp.text = POST_RESP

        def delete(self, req, resp):
            resp.text = DELETE_RESP

    assert client.get("http://testserver/book").text == GET_RESP
    assert client.get("http://testserver/book").status_code == 200
    assert client.post("http://testserver/book").text == POST_RESP
    assert client.delete("http://testserver/book").text == DELETE_RESP
    with raises(AttributeError):
        assert client.put("http://testserver/book").text == ''


def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Not found."


def test_alternative_route(api, client):
    response_text = "Alternative way to add a route"

    def home(req, resp):
        resp.text = response_text

    api.add_route("/alternative", home)

    assert client.get("http://testserver/alternative").text == response_text

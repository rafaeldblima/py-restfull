import json

from bson import ObjectId

from api import API
from database.middleware import MingMiddleware
from database.models import Book

app = API(templates_dir="templates")
app.add_middleware(MingMiddleware)


@app.route("/home")
def home(request, response):
    response.body = app.template("home.html", context={"title": "Py-restfull Framework", "name": "py-restfull"})


@app.route("/book")
class BooksHandler:
    def get(self, req, resp, pk=None):
        if pk:
            json = Book.query.get(_id=ObjectId(pk)).dictify()
        else:
            json = [book.dictify() for book in Book.query.find().all()]
        resp.json = json

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

    def delete(self, req, resp):
        resp.text = "Endpoint to delete a book"

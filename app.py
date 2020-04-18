from bson import ObjectId

from api import API
from database.middleware import MingMiddleware
from database.models import Book

app = API(templates_dir="templates")
app.add_middleware(MingMiddleware)


@app.route("/home")
def home(request, response):
    response.body = app.template("home.html", context={"title": "Py-restfull Framework", "name": "py-restfull"})


@app.route("/book/average-price")
def average_price(req, res):
    result = list(
        Book.query.aggregate(
            [
                {'$match': {'price': {'$gt': 0}}},
                {'$group': {'_id': None, 'count': {"$avg": {"$toDecimal": "$price"}}}}
            ]
        )
    )
    if result:
        res.json = {'average': float(str(result[0].get('count')))}
    else:
        res.status_code = 204


@app.route("/book")
class BooksHandler:
    def get(self, req, resp, pk=None):
        if pk:
            json = Book.query.get(_id=ObjectId(pk)).dictify()
        else:
            json = [book.dictify() for book in Book.query.find().all()]
        resp.json = json

    def post(self, req, resp):
        b = Book(**req.json)
        resp.json = b.dictify()

    def delete(self, req, resp, pk):
        book = Book.query.get(_id=ObjectId(pk))
        book.delete()
        resp.status_code = 204

    def put(self, req, resp, pk):
        req_body = req.json
        properties_to_update = Book.get_all_properties()
        if all(x in req_body for x in properties_to_update):
            book = Book.query.get(_id=ObjectId(pk))
            for key, value in req_body.items():
                setattr(book, key, value)
            resp.json = book.dictify()

    def patch(self, req, resp, pk):
        req_body = req.json
        book = Book.query.get(_id=ObjectId(pk))
        for key, value in req_body.items():
            setattr(book, key, value)
        resp.json = book.dictify()

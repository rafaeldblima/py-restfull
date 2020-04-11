from api import API
from middleware import Middleware

app = API(templates_dir="templates")


@app.route("/home")
def home(request, response):
    response.body = app.template("home.html", context={"title": "Py-restfull Framework", "name": "py-restfull"})


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"


@app.route("/hello/{name}")
def say_hello(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/tell/{age:d}")
def tell(request, response, age):
    response.text = f"Your age: {age}"


@app.route("/book")
class BooksHandler:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

    def delete(self, req, resp):
        resp.text = "Endpoint to delete a book"


def custom_exception_handler(request, response, exception_cls):
    response.text = "Oops! Something went wrong."


app.add_exception_handler(custom_exception_handler)


@app.route("/error")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be user")


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, res):
        print("Processing response", req.url)


app.add_middleware(SimpleCustomMiddleware)

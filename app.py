from api import API

app = API()


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


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

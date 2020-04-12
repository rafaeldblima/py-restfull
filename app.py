from api import API

app = API(templates_dir="templates")


@app.route("/home")
def home(request, response):
    response.body = app.template("home.html", context={"title": "Py-restfull Framework", "name": "py-restfull"})


@app.route("/book")
class BooksHandler:
    def get(self, req, resp):
        resp.body = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

    def delete(self, req, resp):
        resp.text = "Endpoint to delete a book"

from api import API

app = API(templates_dir="templates")


@app.route("/home")
def home(request, response):
    response.body = app.template("home.html", context={"title": "Py-restfull Framework", "name": "py-restfull"})

import os

from parse import parse
from requests import Session
from whitenoise import WhiteNoise
from wsgiadapter import WSGIAdapter

from middleware import Middleware
from utils import cut_static_root, empty_wsgi_app, request_for_static
from utils.error_handlers import debug_exception_handler
from utils.exceptions import HTTPError
from utils.response import Response
from utils.routes import Route
from utils.templates import get_templates_env


class API:

    def __init__(self, templates_dir='templates', static_dir="static", debug: bool = False):
        self.templates = get_templates_env(os.path.abspath(templates_dir))
        self._routes = {}
        self._exception_handler = None
        self.static_dir = os.path.abspath(static_dir)
        self._static_root = "/static"
        self._middleware = Middleware(self)
        self._debug = debug

    @property
    def debug(self):
        return self._debug

    def add_middleware(self, middleware_cls):
        self._middleware.add(middleware_cls)

    def add_exception_handler(self, exception_handler):
        self._exception_handler = exception_handler

    def find_handler(self, request_path):
        for path, handler in self._routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def _handle_exception(self, request, response, exception):
        if self._exception_handler is not None:
            self._exception_handler(request, response, exception)
        else:
            if self._debug is False:
                raise exception

            debug_exception_handler(request, response, exception)

    def find_route(self, path):
        for pattern, route in self._routes.items():
            matched, kwargs = route.match(request_path=path)
            if matched is True:
                return route, kwargs

        return None, {}

    def dispatch_request(self, request):
        response = Response()

        route, kwargs = self.find_route(path=request.path)

        try:
            if route is None:
                raise HTTPError(status=404)

            route.handle_request(request, response, **kwargs)
        except Exception as e:
            self._handle_exception(request, response, e)

        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def add_route(self, pattern, handler, methods=None, detail=False):
        """ Add a new route """
        assert pattern not in self._routes, f"Duplicated route: {pattern}"

        self._routes[pattern] = Route(path_pattern=pattern, handler=handler, methods=methods, detail=detail)

    def route(self, path, methods=None, detail=False):
        """ Decorator that adds a new route """

        def wrapper(handler):
            self.add_route(path, handler, methods, detail)
            return handler

        return wrapper

    def session(self, base_url="http://testserver"):
        session = Session()
        session.mount(prefix=base_url, adapter=WSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates.get_template(template_name).render(**context).encode()

    def as_whitenoise_app(self, environ, start_response):
        white_noise = WhiteNoise(empty_wsgi_app(), root=self.static_dir)
        return white_noise(environ, start_response)

    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]

        if request_for_static(path_info, self._static_root):
            environ["PATH_INFO"] = cut_static_root(path_info, self._static_root)
            return self.as_whitenoise_app(environ, start_response)

        return self._middleware(environ, start_response)

from http import HTTPStatus
from inspect import isclass

from parse import parse

from utils.constants import ALL_HTTP_METHODS
from utils.exceptions import HTTPError


class Route:
    PK_METHODS = ['PUT', 'PATCH', 'DELETE', 'OPTIONS', 'GET']

    def __init__(self, path_pattern, handler, methods=None, detail=False):
        if methods is None:
            methods = ALL_HTTP_METHODS

        if (any(True for x in methods if x in self.PK_METHODS) and isclass(handler)) or detail:
            self._patterns = [path_pattern, path_pattern + '/', path_pattern + '/{pk}']
        else:
            self._patterns = [path_pattern, path_pattern + '/']
        self._handler = handler
        self._methods = [method.upper() for method in methods]

    def match(self, request_path):
        result = None
        for pattern in self._patterns:
            result = parse(pattern, request_path)
            if result:
                break
        if result is not None:
            return True, result.named

        return False, None

    def handle_request(self, request, response, **kwargs):
        if isclass(self._handler):
            handler = getattr(self._handler(), request.method.lower(), None)
            if handler is None:
                raise HTTPError(status=HTTPStatus.METHOD_NOT_ALLOWED)
        else:
            if request.method not in self._methods:
                raise HTTPError(status=HTTPStatus.METHOD_NOT_ALLOWED)

            handler = self._handler

        handler(request, response, **kwargs)

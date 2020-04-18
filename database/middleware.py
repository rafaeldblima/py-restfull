from api import Middleware
from database.session import session


class MingMiddleware(Middleware):
    def process_response(self, req, res):
        session.flush_all()
        session.close()

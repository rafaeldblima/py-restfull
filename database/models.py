from ming import schema
from ming.odm import FieldProperty
from ming.odm import MappedClass

from .session import session


class Book(MappedClass):
    class __mongometa__:
        session = session
        name = 'book'

    _id = FieldProperty(schema.ObjectId)
    title = FieldProperty(schema.String(required=True))
    description = FieldProperty(schema.String(if_missing=''))

from datetime import datetime

from ming.odm import FieldProperty, MappedClass, ThreadLocalODMSession, MapperExtension
from ming.schema import ObjectId, String, NumberDecimal, DateTime

from .session import session


class BaseClass(MappedClass):
    class __mongometa__:
        session: ThreadLocalODMSession = None
        name = None

    def save(self):
        self.__mongometa__.session.flush_all()


class UpdatedAtExtension(MapperExtension):
    def before_update(self, instance, state, sess):
        print('passou')
        instance.updated_at = datetime.utcnow()


class Timeable(MappedClass):
    created_at = FieldProperty(DateTime(if_missing=datetime.utcnow))
    updated_at = FieldProperty(DateTime(if_missing=datetime.utcnow))

    class __mongometa__:
        extensions = [UpdatedAtExtension]


class Book(BaseClass, Timeable):
    class __mongometa__:
        session: ThreadLocalODMSession = session
        name = 'book'

    _id = FieldProperty(ObjectId)
    title = FieldProperty(String(required=True))
    description = FieldProperty(String(if_missing=''))
    price = FieldProperty(NumberDecimal(if_missing=0.0, precision=2))

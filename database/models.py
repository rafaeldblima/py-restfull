import inspect
from datetime import datetime
from decimal import Decimal

from bson import Decimal128
from bson import ObjectId as obj_id
from ming.odm import FieldProperty, MappedClass, ThreadLocalODMSession, MapperExtension, mapper
from ming.schema import ObjectId, String, NumberDecimal, DateTime

from .session import session


class BaseClass(MappedClass):
    class __mongometa__:
        session: ThreadLocalODMSession = None
        name = None

    def save(self):
        self.__mongometa__.session.flush_all()

    def dictify(self):
        prop_names = [prop.name for prop in mapper(self).properties
                      if isinstance(prop, FieldProperty)]
        props = {}
        for key in prop_names:
            props[key] = getattr(self, key)
            if isinstance(props[key], obj_id):
                props[key] = str(props.get(key))
            elif isinstance(props[key], datetime):
                props[key] = props[key].isoformat()
            elif isinstance(props[key], Decimal128) or isinstance(props[key], Decimal):
                props[key] = float(str(props[key]))
        return props

    @classmethod
    def get_all_properties(cls):
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        attributes = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
        # TODO: alterar fieldProperty caso tenha algum outro tipo de campo
        return [a[0] for a in attributes if
                isinstance(a[1], FieldProperty) and a[0] != 'created_at' and a[0] != 'updated_at' and a[0] != '_id'
                ]


class UpdatedAtExtension(MapperExtension):
    def before_update(self, instance, state, sess):
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

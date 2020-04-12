from ming import create_datastore
from ming.odm import ThreadLocalODMSession

from api import DATABASE

session = ThreadLocalODMSession(
    bind=create_datastore(
        f'mongodb://{DATABASE.user}:{DATABASE.password}@'
        f'{DATABASE.host}:{DATABASE.port}/{DATABASE.dbname}?authSource=admin'
    )
)

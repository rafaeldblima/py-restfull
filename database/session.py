from ming import create_datastore
from ming.odm import ThreadLocalODMSession

session = ThreadLocalODMSession(
    bind=create_datastore('mongodb://local:123456@localhost:27018/local?authSource=admin')
)

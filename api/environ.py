import os

import environ

from api.models import Database

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
envfile_path = os.path.join(BASE_DIR, 'infra/.env')
env.read_env(env_file=envfile_path)

DATABASE = Database(
    env('DATABASE_NAME'),
    env('DATABASE_USERNAME'),
    env('DATABASE_PASSWORD'),
    env('DATABASE_HOST'),
    env('DATABASE_PORT')
)

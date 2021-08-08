from .base import *

DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_ENGINE"),
        "NAME": os.getenv("APP_DB_NAME"),
        "USER": os.getenv("APP_DB_USER"),
        "PASSWORD": os.getenv("APP_DB_PASS"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

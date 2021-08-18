from .base import *

DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_ENGINE"),
        "NAME": os.getenv("POSTGRES_NAME"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

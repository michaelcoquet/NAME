from .base import *

DEBUG = False
ADMINS = (("Michael Coquet", "mail@michaelcoquet.ca"),)

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
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

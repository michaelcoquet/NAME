from .base import *

DEBUG = False
ADMINS = (("Michael Coquet", "mail@michaelcoquet.ca"),)
ALLOWED_HOSTS = json.loads(os.getenv("ALLOWED_HOSTS"))
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
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True

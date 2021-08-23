from .base import *
import requests


EC2_PRIVATE_IP = None
try:
    EC2_PRIVATE_IP = requests.get(
        "http://169.254.169.254/latest/meta-data/local-ipv4", timeout=0.01
    ).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

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

BROKER_URL = "sqs://%s:%s@" % (
    os.environ.get("AWS_ACCESS_KEY_ID"),
    os.environ.get("AWS_SECRET_ACCESS_KEY"),
)
CELERY_BROKER_URL = BROKER_URL

CELERY_BROKER_TRANSPORT_OPTIONS = {
    "region": "us-east-1",
    "visibility_timeout": 7200,
    "polling_interval": 1,
    "predefined_queues": {
        "celery": {
            "url": "https://sqs.us-east-1.amazonaws.com/405486787066/namedb_task_q",
            "access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
            "secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        }
    },
}

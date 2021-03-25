import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = secrets.token_urlsafe(32)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

INSTALLED_APPS = ("db",)
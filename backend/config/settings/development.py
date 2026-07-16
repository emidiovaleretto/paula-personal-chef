"""Local development & test settings.

A local, non-deployed environment: an insecure hardcoded SECRET_KEY and SQLite are
acceptable here (constitution §1 — dev DB is the developer's choice). Nothing in this
file is used in a deployed environment.
"""

from .base import *  # noqa: F401,F403
from .base import BASE_DIR

DEBUG = True

# Insecure, development-only key. NOT read from env and NOT used in production.
SECRET_KEY = "django-insecure-dev-only-key-do-not-use-in-production"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Vite dev server origin for the SPA.
CORS_ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]

"""Production settings.

Every secret and environment-specific value is read from the environment and fails
loudly when missing — no hardcoded fallbacks (constitution §1, §6). The database is an
external managed service reached via DATABASE_URL (constitution §6).
"""

from .base import *  # noqa: F401,F403
from .base import env

DEBUG = False

# Fail loudly if unset — `env.str` with no default raises ImproperlyConfigured.
SECRET_KEY = env.str("SECRET_KEY")

# Comma-separated env values, required.
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# External managed PostgreSQL via DATABASE_URL (constitution §6). Required.
DATABASES = {"default": env.db("DATABASE_URL")}

# Explicit, non-wildcard cross-origin config for the SPA. Required.
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# Secure cookies over HTTPS in production. Safe here: no redirect loop, not
# proxy-coupled (the browser<->proxy leg is HTTPS behind a TLS-terminating proxy).
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# NOTE: HTTPS redirect (SECURE_SSL_REDIRECT) and its required companion
# SECURE_PROXY_SSL_HEADER are intentionally NOT set here. Behind a TLS-terminating
# proxy, SECURE_SSL_REDIRECT without the correct SECURE_PROXY_SSL_HEADER causes an
# infinite redirect loop, and the proxy header value is platform-specific. Both are
# owned as a pair by specs/000-platform-setup (see that checklist), to be configured
# once the deploy platform/proxy is chosen (P001).

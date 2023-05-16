from .base import *  # noqa: F401,F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)+g5ge_d87nqw&djyih(5v32h_4fb*&cazz9o3$em8&y2d9x_5"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

# debug
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware"
] + MIDDLEWARE  # noqa: F405
INTERNAL_IPS = ("127.0.0.1",)
INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
]

try:
    from .local import *  # noqa: F401,F403
except ImportError:
    pass

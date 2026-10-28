from settings_base import *  # noqa: F403

DEBUG = True

SECRET_KEY = "dev-only-pyconmz-2027-not-for-production"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "gitignore" / "emails"  # noqa: F405

WAFER_TALKS_OPEN = True
WAFER_REGISTRATION_OPEN = True

INSTALLED_APPS = INSTALLED_APPS + ("debug_toolbar",)  # noqa: F405
MIDDLEWARE = (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,  # noqa: F405
)
INTERNAL_IPS = ["127.0.0.1"]
ALLOWED_HOSTS = [*ALLOWED_HOSTS, "testserver"]
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "website.debug.show_toolbar",
}

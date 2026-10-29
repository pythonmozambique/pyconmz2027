import os

from settings_base import *  # noqa: F403

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


def _csrf_origin(host):
    if host == "*":
        return ""
    if host.startswith("."):
        return f"https://*{host}"
    return f"https://{host}"


CSRF_TRUSTED_ORIGINS = [
    origin for origin in (_csrf_origin(host) for host in ALLOWED_HOSTS) if origin  # noqa: F405
]
WAFER_TALKS_OPEN = os.environ.get("WAFER_TALKS_OPEN", "").lower() in {"1", "true", "yes"}
WAFER_REGISTRATION_OPEN = os.environ.get("WAFER_REGISTRATION_OPEN", "").lower() in {
    "1",
    "true",
    "yes",
}

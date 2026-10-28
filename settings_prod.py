import os

from settings_base import *  # noqa: F403

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]
WAFER_TALKS_OPEN = os.environ.get("WAFER_TALKS_OPEN", "").lower() in {"1", "true", "yes"}
WAFER_REGISTRATION_OPEN = os.environ.get("WAFER_REGISTRATION_OPEN", "").lower() in {
    "1",
    "true",
    "yes",
}

import os
from pathlib import Path
from urllib.parse import urlparse

import django.utils.translation as translation
from django.urls import reverse_lazy
from django.utils.functional import lazy


def _gettext_when_ready(message):
    """Translate only after Django has loaded its applications.

    Vercel stringifies settings before django.setup(). A normal gettext_lazy
    call at that moment raises AppRegistryNotReady.
    """
    from django.apps import apps

    if not apps.ready:
        return message
    return translation.gettext(message)


translation.gettext_lazy = lazy(_gettext_when_ready, str)
from django.utils.translation import gettext_lazy as _  # noqa: E402

from wafer.settings import *  # noqa: E402,F403

CONFERENCE_NAME = "PyCon Mozambique 2027"
# CONFERENCE_DATES = "14–17 October 2027"
CONFERENCE_DATES = _("To be announced")
CONFERENCE_CITY = "Maputo"
# CONFERENCE_VENUE = "CCFM & Joaquim Chissano Centre, Maputo"
CONFERENCE_VENUE = _("To be announced")
# CFP_DEADLINE = "15 May 2027"
CFP_DEADLINE = _("To be announced")

BASE_DIR = Path(__file__).resolve().parent

ROOT_URLCONF = "urls"
WSGI_APPLICATION = "wafer.wsgi.application"

DATABASES["default"]["NAME"] = BASE_DIR / "db.sqlite3"  # noqa: F405

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "dev-only-pyconmz-2027-change-me",
)

ALLOWED_HOSTS = [
    host
    for host in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host
]

DEBUG = False

INSTALLED_APPS = (
    "template_partials",
    "django_cotton",
    "website",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.redirects",
    "reversion",
    "bakery",
    "crispy_forms",
    "crispy_tailwind",
    "crispy_bootstrap5",
    "rest_framework",
    "django_select2",
    "wafer",
    "wafer.kv",
    "wafer.registration",
    "wafer.talks",
    "wafer.schedule",
    "wafer.users",
    "wafer.sponsors",
    "wafer.pages",
    "wafer.tickets",
    "wafer.compare",
    "markitup",
    "registration",
    "django.contrib.admin",
    "django_browser_reload",
)

TEMPLATES = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "wafer.context_processors.site_info",
                "wafer.context_processors.navigation_info",
                "wafer.context_processors.menu_info",
                "wafer.context_processors.registration_settings",
                "context.conference",
            ),
            "builtins": [
                "django_browser_reload.templatetags.django_browser_reload",
            ],
        },
    },
]

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
)

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "localstatic"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "localmedia"
BUILD_DIR = str(BASE_DIR / "mirror")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = ("tailwind", "bootstrap5")
CRISPY_TEMPLATE_PACK = "tailwind"
COTTON_SNAKE_CASED_NAMES = False

USE_TZ = True
TIME_ZONE = "Africa/Maputo"
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", _("English")),
    ("pt", _("Portuguese")),
]
LOCALE_PATHS = [BASE_DIR / "locale"]

WAFER_TALK_LANGUAGES = (
    ("en", _("English")),
    ("pt", _("Portuguese")),
)

MARKITUP_FILTER = (
    "markdown.markdown",
    {
        "extensions": [
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            "mdx_variables",
            "mdx_staticfiles",
        ],
        "extension_configs": {
            "mdx_variables": {"vars": {}},
        },
    },
)
WAFER_PAGE_MARKITUP_FILTER = MARKITUP_FILTER

WAFER_CONFERENCE_ACRONYM = "PyCon MZ"
WAFER_DYNAMIC_MENUS = ("wafer.pages.models.page_menus",)
WAFER_HIDE_LOGIN = False
WAFER_TALKS_OPEN = False
WAFER_REGISTRATION_OPEN = False
WAFER_PUBLIC_ATTENDEE_LIST = False

WAFER_MENUS = (
    {
        "label": _("About"),
        "url": reverse_lazy("wafer_page", args=("about",)),
    },
    {
        "label": _("Keynotes"),
        "url": reverse_lazy("wafer_talks_speakers"),
    },
    {
        "label": _("Schedule"),
        "url": reverse_lazy("wafer_full_schedule"),
    },
    {
        "label": _("Call for Proposals"),
        "url": reverse_lazy("wafer_page", args=("call-for-proposals",)),
    },
    {
        "label": _("Sponsors"),
        "url": reverse_lazy("wafer_sponsors"),
    },
    {
        "label": _("Location"),
        "url": reverse_lazy("wafer_page", args=("location",)),
    },
)

SOCIAL_LINKS = (
    {"name": "WhatsApp", "url": "https://chat.whatsapp.com/Lqlzo70Im7B8DzXLWWFKsX"},
    {"name": "GitHub", "url": "https://github.com/pythonmozambique"},
    {"name": "Instagram", "url": "https://www.instagram.com/pythonmozambique"},
    {"name": "LinkedIn", "url": "https://www.linkedin.com/company/pythonmozambique"},
    {"name": "Discord", "url": "https://discord.gg/yrmQa8tQ8D"},
    {"name": "Meetup", "url": "https://www.meetup.com/pythonmozambique/"},
    {"name": "X", "url": "https://x.com/pythonmoz"},
)

CONTACT_US_EMAILS = {
    "team": "python.community.moz@gmail.com",
    "sponsorship": "python.community.moz@gmail.com",
}

# Public pass copy. Wafer ticket records (claims) are created in the admin
# and do not store a price, so the published offer lives with the site.
TICKET_OFFERS = (
    {
        "name": _("Academic & Student"),
        "price": "1,500",
        "currency": "MZN",
        "usd": "~$24 USD",
        "summary": _("For enrolled university students, high school students, and recent graduates seeking employment."),
        "includes": (
            _("All 4-day sessions and keynotes"),
            _("Official PyCon MZ badge"),
            _("Career fair and speed mentoring"),
        ),
    },
    {
        "name": _("Individual"),
        "price": "4,500",
        "currency": "MZN",
        "usd": "~$70 USD",
        "summary": _("For engineers, freelancers, hobbyists, and community contributors paying out of pocket."),
        "includes": (
            _("Full conference, workshops and sprints"),
            _("Daily lunch, coffee breaks and mixer"),
            _("Opening reception invite"),
        ),
        "featured": True,
    },
    {
        "name": _("Company / Corporate"),
        "price": "12,000",
        "currency": "MZN",
        "usd": "~$188 USD",
        "summary": _("For staff whose company covers admission. Funds the diversity grant programme."),
        "includes": (
            _("All-access pass and VAT invoice"),
            _("Networking lounge access"),
            _("Subsidises 2 full student scholarships"),
        ),
    },
)

BAKERY_VIEWS = (
    "wafer.pages.views.ShowPage",
    "wafer.schedule.views.VenueView",
    "wafer.schedule.views.ScheduleView",
    "wafer.schedule.views.ScheduleXmlView",
    "wafer.schedule.views.ICalView",
    "wafer.sponsors.views.ShowSponsors",
    "wafer.sponsors.views.ShowPackages",
    "wafer.sponsors.views.SponsorView",
    "wafer.talks.views.TalkView",
    "wafer.talks.views.Speakers",
    "wafer.talks.views.TracksView",
    "wafer.talks.views.TalkTypesView",
    "wafer.talks.views.UsersTalks",
    "wafer.users.views.UsersView",
    "wafer.users.views.ProfileView",
    "website.views.PageHome",
)


def _database_from_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in {"postgres", "postgresql"}:
        return None
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": parsed.path.lstrip("/"),
        "USER": parsed.username or "",
        "PASSWORD": parsed.password or "",
        "HOST": parsed.hostname or "",
        "PORT": str(parsed.port or ""),
    }


_database_url = os.environ.get("DATABASE_URL")
if _database_url:
    _parsed_database = _database_from_url(_database_url)
    if _parsed_database:
        DATABASES["default"] = _parsed_database  # noqa: F405

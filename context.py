import json

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage


def site_origin(request):
    """Public origin for canonical and social URLs.

    CANONICAL_ORIGIN wins when it is set, so a preview host does not become
    the indexed URL. Otherwise the request host is used.
    """
    if settings.CANONICAL_ORIGIN:
        return settings.CANONICAL_ORIGIN
    return request.build_absolute_uri("/").rstrip("/")


def absolute_url(request, path):
    if path.startswith(("http://", "https://")):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return site_origin(request) + path


def conference(request):
    """Conference facts used by the shared header, footer, and home page."""
    language = getattr(request, "LANGUAGE_CODE", "") or settings.LANGUAGE_CODE
    image = staticfiles_storage.url("img/pythonmozambique-logo.png")
    payload = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": settings.CONFERENCE_NAME,
        "url": site_origin(request) + "/",
    }
    website_ld = (
        json.dumps(payload, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )
    return {
        "SOCIAL_LINKS": settings.SOCIAL_LINKS,
        "CONFERENCE_NAME": settings.CONFERENCE_NAME,
        "CONFERENCE_DATES": settings.CONFERENCE_DATES,
        "CONFERENCE_VENUE": settings.CONFERENCE_VENUE,
        "CONFERENCE_CITY": settings.CONFERENCE_CITY,
        "CFP_DEADLINE": settings.CFP_DEADLINE,
        "CONTACT_US_EMAILS": settings.CONTACT_US_EMAILS,
        "META_DESCRIPTION": settings.META_DESCRIPTION,
        "canonical_url": absolute_url(request, request.path or "/"),
        "og_image_url": absolute_url(request, image),
        "og_locale": "pt_PT" if language.startswith("pt") else "en_US",
        "website_ld_json": website_ld,
    }

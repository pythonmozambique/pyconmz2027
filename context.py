from django.conf import settings


def conference(request):
    """Conference facts used by the shared header, footer, and home page."""
    return {
        "SOCIAL_LINKS": settings.SOCIAL_LINKS,
        "CONFERENCE_DATES": settings.CONFERENCE_DATES,
        "CONFERENCE_VENUE": settings.CONFERENCE_VENUE,
        "CONFERENCE_CITY": settings.CONFERENCE_CITY,
        "CFP_DEADLINE": settings.CFP_DEADLINE,
        "CONTACT_US_EMAILS": settings.CONTACT_US_EMAILS,
    }

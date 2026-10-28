from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from wafer.sponsors.models import SponsorshipPackage
from wafer.talks.models import TalkType, Track
from wafer.tickets.models import TicketType


TALK_TYPES = (
    {
        "name": "Keynote",
        "description": "Invited plenary talks. Added by the programme team, not the public call.",
        "order": 1,
        "disable_submission": True,
    },
    {
        "name": "Talk",
        "description": "A 30-minute conference talk with questions.",
        "order": 2,
        "disable_submission": False,
    },
    {
        "name": "Tutorial",
        "description": "A 90-minute hands-on workshop.",
        "order": 3,
        "disable_submission": False,
    },
    {
        "name": "Lightning",
        "description": "A short lightning talk.",
        "order": 4,
        "disable_submission": False,
    },
)

TRACKS = (
    {
        "name": "Web Development & APIs",
        "description": "Async web frameworks, APIs, and real-time systems.",
        "order": 1,
    },
    {
        "name": "Data Science & AI / ML",
        "description": "Data analysis, machine learning, and practical modelling.",
        "order": 2,
    },
    {
        "name": "DevOps, Cloud & Reliability",
        "description": "Shipping, observing, and operating Python in production.",
        "order": 3,
    },
    {
        "name": "Community & Open Source",
        "description": "Community building, governance, and open-source contribution.",
        "order": 4,
    },
    {
        "name": "Python in Education & IoT",
        "description": "Teaching Python and building with hardware.",
        "order": 5,
    },
)

PACKAGES = (
    {
        "name": "Baobab (Diamond)",
        "order": 1,
        "short_description": "Lead partnership for the inaugural PyCon Mozambique.",
        "symbol": "◆",
    },
    {
        "name": "Acacia (Platinum)",
        "order": 2,
        "short_description": "Platinum support for talks, travel, and community grants.",
        "symbol": "●",
    },
    {
        "name": "Maputo Bay (Gold)",
        "order": 3,
        "short_description": "Gold support for local developers and student access.",
        "symbol": "★",
    },
)

TICKET_NAMES = (
    "Academic & Student",
    "Individual",
    "Company / Corporate",
)

# English text stored in the database. The public site translates these
# msgids at display time. Keep the stored values in English.
CATALOGUE_MSGIDS = (
    _("Keynote"),
    _("Invited plenary talks. Added by the programme team, not the public call."),
    _("Talk"),
    _("A 30-minute conference talk with questions."),
    _("Tutorial"),
    _("A 90-minute hands-on workshop."),
    _("Lightning"),
    _("A short lightning talk."),
    _("Web Development & APIs"),
    _("Async web frameworks, APIs, and real-time systems."),
    _("Data Science & AI / ML"),
    _("Data analysis, machine learning, and practical modelling."),
    _("DevOps, Cloud & Reliability"),
    _("Shipping, observing, and operating Python in production."),
    _("Community & Open Source"),
    _("Community building, governance, and open-source contribution."),
    _("Python in Education & IoT"),
    _("Teaching Python and building with hardware."),
    _("Baobab (Diamond)"),
    _("Lead partnership for the inaugural PyCon Mozambique."),
    _("Acacia (Platinum)"),
    _("Platinum support for talks, travel, and community grants."),
    _("Maputo Bay (Gold)"),
    _("Gold support for local developers and student access."),
)


class Command(BaseCommand):
    help = "Create talk types, tracks, sponsorship tiers, and ticket type names. Does not invent speakers or sponsors."

    def handle(self, *args, **options):
        for row in TALK_TYPES:
            TalkType.objects.update_or_create(
                name=row["name"],
                defaults={
                    "description": row["description"],
                    "order": row["order"],
                    "disable_submission": row["disable_submission"],
                },
            )
        for row in TRACKS:
            Track.objects.update_or_create(
                name=row["name"],
                defaults={
                    "description": row["description"],
                    "order": row["order"],
                },
            )
        for row in PACKAGES:
            SponsorshipPackage.objects.update_or_create(
                name=row["name"],
                defaults={
                    "order": row["order"],
                    "number_available": None,
                    "currency": "MZN",
                    "price": Decimal("0"),
                    "short_description": row["short_description"],
                    "description": row["short_description"],
                    "symbol": row["symbol"],
                },
            )
        for name in TICKET_NAMES:
            TicketType.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Conference catalogue is ready."))

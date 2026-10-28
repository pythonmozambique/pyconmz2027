from datetime import datetime, timezone

from bakery.views import BuildableTemplateView
from django.conf import settings

from wafer.schedule.models import ScheduleItem
from wafer.sponsors.models import SponsorshipPackage
from wafer.talks.models import ACCEPTED, Talk
from wafer.talks.models import Track


def _initials(name):
    parts = [part for part in name.split() if part]
    if not parts:
        return "?"
    return "".join(part[0] for part in parts[:2]).upper()


def _talk_card(talk):
    speakers = talk.get_authors_display_name() or talk.get_corresponding_author_name()
    return {
        "title": talk.title,
        "url": talk.get_absolute_url(),
        "speakers": speakers,
        "initials": _initials(speakers),
        "type": talk.talk_type.name if talk.talk_type_id else "",
        "track": talk.track.name if talk.track_id else "",
    }


def _item_start(item):
    starts = [
        slot.get_start_time()
        for slot in item.slots.all()
        if slot.get_start_time()
    ]
    return min(starts) if starts else None


class PageHome(BuildableTemplateView):
    template_name = "website/page_home.html"
    build_path = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keynotes = (
            Talk.objects.filter(status=ACCEPTED, talk_type__name__iexact="Keynote")
            .select_related("talk_type", "track", "corresponding_author")
            .prefetch_related("authors", "authors__userprofile")
            .order_by("title")
        )
        items = list(
            ScheduleItem.objects.filter(talk__status=ACCEPTED)
            .select_related(
                "talk",
                "talk__talk_type",
                "talk__corresponding_author",
                "venue",
            )
            .prefetch_related("slots", "talk__authors", "talk__authors__userprofile")
        )
        far_future = datetime(9999, 1, 1, tzinfo=timezone.utc)
        dated = []
        for item in items:
            if not item.talk_id:
                continue
            start = _item_start(item)
            dated.append((start or far_future, start, item))
        dated.sort(key=lambda pair: pair[0])
        preview = []
        for _order, start, item in dated[:6]:
            card = _talk_card(item.talk)
            card["starts_at"] = start
            card["venue"] = item.venue.name
            preview.append(card)

        context.update(
            {
                "keynotes": [_talk_card(talk) for talk in keynotes],
                "schedule_preview": preview,
                "sponsor_packages": SponsorshipPackage.objects.prefetch_related("sponsors"),
                "tracks": Track.objects.all(),
                "ticket_offers": settings.TICKET_OFFERS,
                # Restore with the commented calendar block in page_home.html.
                # "phases": (
                #     {
                #         "label": "Phase 01",
                #         "state": "Active",
                #         "when": "15 May 2027",
                #         "title": "CFP submissions close",
                #         "detail": "Final deadline for 30-minute talks, 90-minute workshops, and lightning ideas.",
                #     },
                #     {
                #         "label": "Phase 02",
                #         "state": "Upcoming",
                #         "when": "30 June 2027",
                #         "title": "Schedule announced",
                #         "detail": "Speaker notifications go out and the multitrack agenda is published from the schedule.",
                #     },
                #     {
                #         "label": "Phase 03",
                #         "state": "Day 1",
                #         "when": "14 October 2027",
                #         "title": "Workshops",
                #         "detail": "Hands-on tutorials and community sprints at the Centro Cultural Franco-Moçambicano.",
                #     },
                #     {
                #         "label": "Phase 04",
                #         "state": "Days 2 & 3",
                #         "when": "15–16 October 2027",
                #         "title": "Main conference",
                #         "detail": "Keynotes, breakout talks, and the opening gathering at the Joaquim Chissano Centre.",
                #     },
                #     {
                #         "label": "Phase 05",
                #         "state": "Day 4",
                #         "when": "17 October 2027",
                #         "title": "Open source sprints",
                #         "detail": "A collaboration day for libraries, documentation, and work alongside maintainers.",
                #     },
                # ),
            }
        )
        return context

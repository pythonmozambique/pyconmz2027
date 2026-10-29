from xml.sax.saxutils import escape

from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

from context import absolute_url

SITEMAP_ROUTES = (
    ("page_home", ()),
    ("wafer_page", ("about",)),
    ("wafer_page", ("location",)),
    ("wafer_page", ("call-for-proposals",)),
    ("wafer_page", ("code-of-conduct",)),
    ("wafer_talks_speakers", ()),
    ("wafer_full_schedule", ()),
    ("wafer_sponsors", ()),
)


@require_GET
def robots(request):
    sitemap = absolute_url(request, reverse("sitemap"))
    body = f"User-agent: *\nAllow: /\n\nSitemap: {sitemap}\n"
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


@require_GET
def sitemap(request):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for name, args in SITEMAP_ROUTES:
        loc = escape(absolute_url(request, reverse(name, args=args)))
        lines.append(f"  <url><loc>{loc}</loc></url>")
    lines.append("</urlset>")
    return HttpResponse("\n".join(lines) + "\n", content_type="application/xml; charset=utf-8")

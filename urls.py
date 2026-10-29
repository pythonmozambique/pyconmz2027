import django
from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

if not apps.ready:
    django.setup()

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    re_path(r"^accounts/", include("wafer.registration.urls")),
    re_path(r"^users/", include("wafer.users.urls")),
    re_path(r"^talks/", include("wafer.talks.urls")),
    re_path(r"^sponsors/", include("wafer.sponsors.urls")),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^markitup/", include("markitup.urls")),
    re_path(r"^schedule/", include("wafer.schedule.urls")),
    re_path(r"^tickets/", include("wafer.tickets.urls")),
    re_path(r"^kv/", include("wafer.kv.urls")),
    path("", include("website.urls")),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Pages occupy the remaining URL space and must come last.
urlpatterns.append(re_path(r"", include("wafer.pages.urls")))

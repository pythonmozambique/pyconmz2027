from django.urls import path

from . import seo, views

urlpatterns = [
    path("robots.txt", seo.robots, name="robots"),
    path("sitemap.xml", seo.sitemap, name="sitemap"),
    path("", views.PageHome.as_view(), name="page_home"),
]

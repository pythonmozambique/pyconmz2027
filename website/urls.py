from django.urls import path

from . import views

urlpatterns = [
    path("", views.PageHome.as_view(), name="page_home"),
]

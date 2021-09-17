"""URL Configuration for 'app'."""
from django.urls import path
from django.urls import re_path

from app import views

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    # Matches any html file
    re_path(r"^.*\.html", views.pages, name="pages"),
]

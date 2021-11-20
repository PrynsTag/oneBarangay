"""URL Configuration for 'app'."""
from django.urls import path

from app import views

app_name = "app"

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("about", views.about, name="about"),
    path("work", views.work, name="work"),
    path("pricing", views.pricing, name="pricing"),
    path("contact", views.contact, name="contact"),
]

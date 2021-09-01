"""URL Routing for Appointment."""
from django.urls import path

from . import views

urlpatterns = [path("", views.index)]

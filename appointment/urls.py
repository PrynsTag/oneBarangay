"""URL Routing for Appointment."""
from django.urls import path

from . import views

app_name = "appointment"

urlpatterns = [
    path("view-appointment", views.view_appointment, name="view-appointment")
]

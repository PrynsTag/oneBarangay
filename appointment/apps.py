"""File for Appointment Config."""
from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    """This is Appointment Config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "appointment"

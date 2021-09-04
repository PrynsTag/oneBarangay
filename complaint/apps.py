"""Complaint apps."""
from django.apps import AppConfig


class ComplaintConfig(AppConfig):
    """Complaint config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "complaint"

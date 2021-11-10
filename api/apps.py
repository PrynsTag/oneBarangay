"""File for api config."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Class for api config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

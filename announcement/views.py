"""Create your announcement views here."""
from django.views.generic import TemplateView


class AnnouncementView(TemplateView):
    """Template view for announcement."""

    template_name = "announcement/announcement.html"

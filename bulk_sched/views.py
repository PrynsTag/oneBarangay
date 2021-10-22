"""Create your bulk_sched views here."""
from django.views.generic import TemplateView


class BulkSchedCreateView(TemplateView):
    """Form view for creating bulk scheduling."""

    template_name = "bulk_sched/create.html"

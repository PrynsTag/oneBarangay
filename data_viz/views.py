"""Py file for data_viz views."""
import os

import requests
from django.http import HttpResponse
from django.views.generic import TemplateView

from one_barangay.mixins import ContextPageMixin


# TODO: Implement toggling of charts
class DataVizView(ContextPageMixin, TemplateView):
    """View dashboard.html."""

    template_name = "data_viz/dashboard.html"
    title = "Dashboard"
    sub_title = "Get to know your residents aggregated data."
    segment = "data_viz"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Get context data.

        Args:
          request: The URL request.
          *args: Additional arguments
          **kwargs: Additional keyword arguments.

        Returns:
          The statistics to be generated and displayed to dashboard.html
        """
        context = self.get_context_data()
        if os.getenv("GAE_ENV", "").startswith("standard"):
            url = os.getenv("DATA_VIZ_API")
        else:
            url = "http://localhost:8000/api/data_viz/"

        r = requests.get(url)
        context["stats"] = r.json()

        return self.render_to_response(context)

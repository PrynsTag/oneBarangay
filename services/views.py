"""Hello World."""

from django.shortcuts import render

# Create your views here.


def index(request):
    """Render Service HTML.

    Args:
      request:

    Returns:
      : Display Service Page

    """
    return render(request, "services/service.html")

"""Bulk Schedule views."""
from django.http import HttpResponse

# Create your views here.


def index(request):
    """Sample display for Bulk schedule views.

    Args:
      request:

    Returns: Display bulk schedule
    """
    return HttpResponse("Bulk Schedule Page")

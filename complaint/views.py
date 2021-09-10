"""Complaint views."""
from django.http import HttpResponse

# Create your views here.


def index(request):
    """Sample display for complaint page.

    Args:
      request:

    Returns: This function returns the sample display for complaint page
    """
    return HttpResponse("Complaint ang bebe")

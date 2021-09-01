"""Create your Appointment views here."""
from django.http import HttpResponse


def index(request):
    """Fetch Appointment HTML Pages.

    Args:
      request: The URL Request

    Returns:
      The requested Appointment Page.
    """
    return HttpResponse("Hello! This is Appointments!")

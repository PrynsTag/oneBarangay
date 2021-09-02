"""Create your Appointment views here."""
from django.http import HttpResponse
from django.shortcuts import render


def view_appointment(request):
    """Fetch Appointment HTML Pages.

    Args:
      request: The URL Request

    Returns:
      The requested Appointment Page.
    """
    # return HttpResponse("Hello! This is Appointments!")
    return render(request, "appointment/home.html")

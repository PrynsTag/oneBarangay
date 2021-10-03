"""Services views.."""

import datetime

from django.shortcuts import render

from appointment.custom_class.firestore_data import FirestoreData


def index(request):
    """Render Service HTML.

    Args:
      request:

    Returns:
      : Display Service Page
    """
    search = FirestoreData()

    year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day

    full_datetime = datetime.datetime(year=year, month=month, day=day)

    date = datetime.date(year=year, month=month, day=day)

    count, appointment_list = search.day_appointments(date=full_datetime, utc_offset=8)

    return render(
        request,
        "services/service.html",
        {
            "active_appointments": count if appointment_list != [] else 0,
            "current_date": date,
        },
    )

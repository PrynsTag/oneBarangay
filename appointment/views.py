"""Create your Appointment views here."""
import datetime
from collections import OrderedDict

# Firebase
from django.shortcuts import render
from firebase_admin import firestore
from firebase_admin.exceptions import AlreadyExistsError

from auth.service_account import firebase_authentication
from custom_class.date_formatter import Date_Formatter

# Custom Class
from custom_class.encrypter import Encrypter

# Globals
app = firebase_authentication()
db = firestore.client(app)

working_hours = [
    "1300",
    "0800",
    "0900",
    "1000",
    "1100",
    "1200",
    "0700",
    "1400",
    "1500",
    "1600",
    "1700",
]


def view_appointment(request):
    """Display the list of appointments.

    Args:
      request: The URL request.

    Returns:
      The view_appointment template and the appointments and working hours context data.
    """
    result_dict = None

    try:
        doc_ref = db.collection("appointments").document(
            (datetime.datetime.now()).strftime("%Y_%m_%d")
        )

        # View Appointment
        doc_result = doc_ref.get()

        if doc_result.exists:
            result_dict = doc_result.to_dict()
        else:
            print("There is no result")

    except AlreadyExistsError:
        print("Account already exists.")

    if result_dict is not None:
        result_dict = OrderedDict(sorted(result_dict.items(), key=lambda x: x))

    return render(
        request,
        "appointment/view_appointment.html",
        {"appointments": result_dict, "time_sorted": sorted(working_hours)},
    )


def details_appointment(request, apt_details):
    """Display the details of the user's appointment.

    Args:
      request: The URL request.
    Returns:
      Renders the html of appointment details
    """
    encrypter = Encrypter(text=apt_details)
    date_formatter = Date_Formatter(full_date=encrypter.code_decoder(), separator="_")
    result_dict = None

    doc_ref_appointment_details = db.collection("appointments").document(
        str(date_formatter.formatted_date)
    )

    doc_appointments = doc_ref_appointment_details.get()

    if doc_appointments.exists:
        result_dict = doc_appointments.to_dict()
    else:
        print("There is no result")

    return render(
        request,
        "appointment/details_appointment.html",
        {"details": result_dict[date_formatter.formatted_time], "amount": "00.00"},
    )

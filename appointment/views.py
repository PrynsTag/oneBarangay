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

def id_verification(request, document_id):
    """Check user ID for verification.

    Args:
      request: Returns: view of appointment details.
      document_id: user appointment document ID

    Returns:
        : change document status
    """
    verify_user = FirestoreData()
    document_id_decrypt = Encrypter(text=document_id).code_decoder()

    if request.method == "POST":
        verification_form = IdVerification(request.POST)

        if verification_form.is_valid():
            field_firstname = verification_form.cleaned_data.get("first_name")
            field_middlename = verification_form.cleaned_data.get("middle_name")
            field_lastname = verification_form.cleaned_data.get("last_name")

            results = verify_user.verify_identification(
                firstname=field_firstname,
                middlename=field_middlename,
                lastname=field_lastname,
            )

            convert_fb_timestamp = DateFormatter(
                full_date=results[0]["created_on"]
            ).date_fb_convert()

            results[0]["created_on"] = convert_fb_timestamp

            if len(results) == 1:
                request.session["user_verified"] = True
                request.session["user_info"] = results[0]
                request.session["document_id"] = document_id_decrypt

                return HttpResponseRedirect(
                    reverse(
                        "appointment:detail-appointment",
                        kwargs={"document_id": document_id},
                    )
                )
            else:
                return HttpResponse("Duplicate user info")
        else:
            return HttpResponse("Invalid input.")
    else:
        verification_form = IdVerification()
        return render(
            request, "appointment/details_appointment.html", {"form", verification_form}
        )


def add_appointment(request):
    """For date testing only.

    Args:
      request: Returns: add date in firestore

    Returns:
        : add account in firebase authentication and firestore
    """
    firestore_add_date = Dummy()
    firestore_add_date.add_appointment_account(time_interval=15, utc_offset=8)

    return HttpResponseRedirect(reverse("services:index"))


def delete_account(request):
    """Delete accounts in authentication and firestore.

    Args:
      request: Returns: delete accounts.

    Returns:
        : delete accounts in firebase authentication and firestore
    """
    search.delete_account_auth()

    return HttpResponse("Account Deleted")


def user_verified(request, document_id):
    """Check user existence.

    Args:
      request: The URL request
      document_id: user appointment document ID

    Returns:
        : Change user's document status
    """
    document_id_decode = Encrypter(text=document_id).code_decoder()

    if "user_verified" in request.session and "document_id" in request.session:
        session_document_id = request.session["document_id"]
        if session_document_id == document_id_decode:
            print("session document id and document id are the same")
        else:
            print("session document id and document are not the same")

    raise Http404("In user verified")

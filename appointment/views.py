"""Create your Appointment views here."""
import datetime
import logging

from one_barangay.scripts.service_account import get_service_from_b64

logger = logging.getLogger(__name__)

# Firebase
from django.shortcuts import Http404, HttpResponse, HttpResponseRedirect, render, reverse

from custom_class.dateformatter import DateFormatter
from custom_class.dummy import Dummy
from custom_class.encrypter import Encrypter
from custom_class.firestore_data import FirestoreData

from .forms import IdVerification

firestoreQuery = FirestoreData()


def view_appointment(request, date):
    """Display the list of appointments.

    Args:
      request: The URL request.
      date: appointment date

    Returns:
      The view_appointment template and the appointments and working hours context data.
    """
    for key in list(request.session.keys()):
        del request.session[key]

    try:
        date_split = date.split("-")
        year = int(date_split[0])
        month = int(date_split[1])
        day = int(date_split[2])

        datetime.datetime(year=year, month=month, day=day)

    except ValueError:
        raise Http404("Page not found")

    else:
        search_date = datetime.date(year=year, month=month, day=day)
        count, appointment_list = firestoreQuery.day_appointments(
            date=search_date, utc_offset=8
        )

        str_date = datetime.date(year=year, month=month, day=day).strftime(
            "%A, %B %d, %Y"
        )

        strp_date = datetime.datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")

        next_date = strp_date + datetime.timedelta(days=1)
        previous_date = strp_date - datetime.timedelta(days=1)

        next_date_formatter = DateFormatter(full_date=next_date)
        previous_date_formatter = DateFormatter(full_date=previous_date)

        next_date_format = next_date_formatter.date_splitter()
        previous_date_format = previous_date_formatter.date_splitter()

        return render(
            request,
            "appointment/view_appointment.html",
            {
                "appointments_list": appointment_list,
                "no_result": count,
                "appointment_date": str(str_date),
                "next_date": next_date_format,
                "previous_date": previous_date_format,
                "current_date": datetime.date.today(),
            },
        )


def request(request, document_id):
    """Display the details of the user's appointment.

    Args:
      request: The URL request.
      document_id: user appointment document ID

    Returns:
      renders the html of appointment details
    """
    form = IdVerification()
    encrypter = Encrypter(text=document_id).code_decoder()

    # Verification
    get_date, get_time, year, month, day, time_int = DateFormatter(
        document_str=encrypter
    ).document_splitter()

    try:
        datetime.date(year=year, month=month, day=day)

    except ValueError:
        raise Http404("Invalid Input")

    else:
        if 0 < time_int < 2300:
            appointment_detail = firestoreQuery.search_appointment(
                document_id=document_id
            )

            start_appointment_formatted = DateFormatter(
                full_date=appointment_detail["start_appointment"]
            ).firebaseTime_formatIt(utc_offset=8)

            end_appointment_formatted = DateFormatter(
                full_date=appointment_detail["end_appointment"]
            ).firebaseTime_formatIt(utc_offset=8)

            createdOn_appointment_formatted = DateFormatter(
                full_date=appointment_detail["created_on"]
            ).firebaseTime_formatIt(utc_offset=8)

            appointment_detail["start_appointment"] = start_appointment_formatted
            appointment_detail["end_appointment"] = end_appointment_formatted
            appointment_detail["created_on"] = createdOn_appointment_formatted

            reschedule = (
                DateFormatter().documentid_to_datetime(document_id=encrypter)
            ).date()

            if "user_check" in request.session and request.session["user_check"]:
                user_list = request.session["user_list"]
                user_verified_session = request.session["user_verified"]

                if user_verified_session:
                    return render(
                        request,
                        "appointment/details_appointment.html",
                        {
                            "reschedule": reschedule,
                            "user_check": True,
                            "user_verified": True,
                            "user_detail": appointment_detail,
                            "user_list": user_list,
                            "amount": 100,
                            "form": form,
                            "back": str(datetime.date(year=year, month=month, day=day)),
                            "document_id": document_id,
                        },
                    )
                else:

                    return render(
                        request,
                        "appointment/details_appointment.html",
                        {
                            "reschedule": reschedule,
                            "user_check": True,
                            "user_verified": False,
                            "user_detail": appointment_detail,
                            "user_list": user_list,
                            "amount": 100,
                            "form": form,
                            "back": str(datetime.date(year=year, month=month, day=day)),
                        },
                    )
            else:

                return render(
                    request,
                    "appointment/details_appointment.html",
                    {
                        "reschedule": reschedule,
                        "user_detail": appointment_detail,
                        "amount": 100,
                        "form": form,
                        "back": str(datetime.date(year=year, month=month, day=day)),
                        "user_check": False,
                    },
                )


def appointment_resched(request, document_id, date):
    """Get appointment lists for reschedule.

    Args:
      request: The URL request.
      document_id: document id in firebase firestore
      date: for list of appointments on a specific date

    Returns:
        list of appointments
    """
    encrypter = Encrypter(text=document_id).code_decoder()
    current_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    resched_list = firestoreQuery.resched_appointment(
        year=current_date.year,
        month=current_date.month,
        day=current_date.day,
        hour=23,
        minute=59,
        second=59,
        document_id=encrypter,
        utc_offset=8,
        datetime=datetime,
        query_list=["start_appointment", "end_appointment", "created_on"],
    )

    next = current_date + datetime.timedelta(days=1)
    previous = current_date - datetime.timedelta(days=1)
    current = (DateFormatter().documentid_to_datetime(document_id=encrypter)).date()
    today = datetime.date.today()

    return render(
        request,
        "appointment/reschedule.html",
        {
            "current_date": current_date.strftime("%B %d, %Y"),
            "appointment_list": resched_list,
            "next": next.date(),
            "previous": previous.date(),
            "current": current,
            "today": today,
            "document_id": document_id,
            "back": document_id,
        },
    )


def id_verification(request, document_id):
    """Check user ID for verification.

    Args:
      request: The URL request.
      document_id: user appointment document ID

    Returns:
      change document status
    """
    document_id_decrypt = Encrypter(text=document_id).code_decoder()

    if request.method == "POST":
        verification_form = IdVerification(request.POST)

        if verification_form.is_valid():
            field_firstname = verification_form.cleaned_data.get("first_name")
            field_middlename = verification_form.cleaned_data.get("middle_name")
            field_lastname = verification_form.cleaned_data.get("last_name")

            # Get results
            results = firestoreQuery.verify_identification(
                firstname=field_firstname,
                middlename=field_middlename,
                lastname=field_lastname,
            )

            user_results = []

            for result in results:
                result["created_on"] = DateFormatter(
                    full_date=result["created_on"]
                ).date_fb_convert()
                user_results.append(result)

            if len(user_results) == 1:
                request.session["user_check"] = True
                request.session["user_verified"] = True
                request.session["user_list"] = user_results
                request.session["document_id"] = document_id_decrypt

                return HttpResponseRedirect(
                    reverse(
                        "appointment:process",
                        kwargs={"document_id": document_id},
                    )
                )
            elif len(user_results) > 1:
                request.session["user_check"] = True
                request.session["user_verified"] = False
                request.session["document_id"] = document_id_decrypt
                request.session["user_list"] = user_results

                return HttpResponseRedirect(
                    reverse(
                        "appointment:process",
                        kwargs={"document_id": document_id},
                    )
                )
            else:
                raise Http404("Data not found.")
        else:
            return HttpResponse("Invalid input.")
    else:
        verification_form = IdVerification()
        return render(
            request, "appointment/details_appointment.html", {"form", verification_form}
        )


def id_verification_manual(request, user_uid):
    """Verify ID of resident if the account exist.

    Args:
      request: The URL request.
      user_uid: user id in firebase firestore

    Returns:
        session indicating that the user was verified
    """
    search_appointment = [firestoreQuery.search_appointment_userId(user_uid=user_uid)]

    user_list = []

    for user in list(search_appointment):
        user["start_appointment"] = DateFormatter(
            full_date=user["start_appointment"]
        ).date_fb_convert()
        user["end_appointment"] = DateFormatter(
            full_date=user["end_appointment"]
        ).date_fb_convert()
        user["created_on"] = DateFormatter(
            full_date=user["created_on"]
        ).date_fb_convert()
        user_list.append(user)

    request.session["user_check"] = True
    request.session["user_verified"] = True
    request.session["user_list"] = user_list
    request.session["document_id"] = search_appointment[0]["document_id"]

    return HttpResponseRedirect(
        reverse(
            "appointment:process",
            kwargs={
                "document_id": Encrypter(
                    text=search_appointment[0]["document_id"]
                ).code_encoder()
            },
        )
    )


def process(request, document_id):
    """Process documents of resident.

    Args:
      request: The URL request.
      document_id: document id of appointment

    Returns:
        document
    """
    return HttpResponse(f"Status: Process, Document ID: {document_id}")


def get(request, document_id):
    """Notify resident if document is already completed.

    Args:
      request: The URL request.
      document_id: document id of appointment collection in firebase firestore

    Returns:
        : sending notification to resident
    """
    return HttpResponse(f"Status: Get, Document ID: {document_id}")


def add_appointment(request):
    """For date testing only.

    Args:
      request: Returns: add date in firestore

    Returns:
      add account in firebase authentication and firestore
    """
    firestore_add_date = Dummy()
    firestore_add_date.add_appointment_account(time_interval=15, utc_offset=8)

    return HttpResponseRedirect(reverse("services:index"))


def delete_account(request):
    """Delete accounts in authentication and firestore.

    Args:
      request: Returns: delete accounts.

    Returns:
      delete accounts in firebase authentication and firestore
    """
    firestoreQuery.delete_account_auth()

    return HttpResponse("Account Deleted")


def user_verified(request, document_id):
    """Check user existence.

    Args:
      request: The URL request
      document_id: user appointment document ID

    Returns:
      Change user's document status
    """
    document_id_decode = Encrypter(text=document_id).code_decoder()

    if "user_verified" in request.session and "document_id" in request.session:

        session_document_id = request.session["document_id"]

        if session_document_id == document_id_decode:
            # user_info = request.session["user_list"]

            # user_uid = user_info[0]["user_uid"]

            print(
                firestoreQuery.search_document(
                    document_id=Encrypter(text=document_id_decode).code_encoder()
                )
            )

            return HttpResponse("User Verified")
def available(
    request,
    old_document_id,
    new_document_id,
):
    """Reschedule appointment.

    Args:
      request: The URL request.
      old_document_id: Recent document ID
      new_document_id: New document ID

    Returns:
        None reschedule appointment
    """
    # check_result = firestoreQuery.reschedule(old_id=old_document_id, new_id=new_document_id)
    return HttpResponse(f"OLD: {old_document_id} | NEW: {new_document_id}")

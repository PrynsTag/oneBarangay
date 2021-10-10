"""Create your Appointment views here."""
import datetime
import logging

# Firebase
from django.http import Http404
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse

from appointment.custom_class.dateformatter import DateFormatter
from appointment.custom_class.dummy import Dummy
from appointment.custom_class.encrypter import Encrypter
from appointment.custom_class.firestore_data import FirestoreData

from .forms import IdVerification

logger = logging.getLogger(__name__)

firestoreQuery = FirestoreData()


def view_appointments(request, date):
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

    except ValueError as invalid_datetime:
        raise Http404 from invalid_datetime

    else:
        search_date = datetime.datetime(year=year, month=month, day=day)
        count, appointment_list = firestoreQuery.day_appointments(date=search_date, utc_offset=8)

        next_date = search_date + datetime.timedelta(days=1)
        previous_date = search_date - datetime.timedelta(days=1)

        next_date_formatter = DateFormatter(full_date=next_date, date=datetime.date.today())
        previous_date_formatter = DateFormatter(
            full_date=previous_date, date=datetime.date.today()
        )

        next_date_format = next_date_formatter.date_splitter()
        previous_date_format = previous_date_formatter.date_splitter()

        return render(
            request,
            "appointment/view_appointments.html",
            {
                "appointments_list": appointment_list,
                "no_result": count,
                "curr_year": year,
                "curr_month": month,
                "curr_day": day,
                "date_isoformat": search_date.isoformat(),
                "next_date": next_date_format,
                "previous_date": previous_date_format,
                "current_date": datetime.date.today(),
                "strf_date": search_date.isoformat(),
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
    full_date = datetime.datetime.now()
    date = datetime.date.today()

    # Verification
    year, month, day, time_int = DateFormatter(
        full_date=full_date, date=date, document_str=encrypter
    ).document_splitter()
    current_user_date = datetime.date(year=year, month=month, day=day)

    try:
        datetime.date(year=year, month=month, day=day)

    except ValueError as invalid_time:
        raise Http404 from invalid_time

    else:

        if 0 < time_int < 2300:
            appointment_detail = firestoreQuery.search_appointment(document_id=document_id)

            start_appointment_formatted = DateFormatter(
                full_date=appointment_detail["start_appointment"], date=date
            ).firebase_time_format(utc_offset=8)

            end_appointment_formatted = DateFormatter(
                full_date=appointment_detail["end_appointment"], date=date
            ).firebase_time_format(utc_offset=8)

            created_apt_formatted = DateFormatter(
                full_date=appointment_detail["created_on"], date=date
            ).firebase_time_format(utc_offset=8)

            appointment_detail["start_appointment"] = start_appointment_formatted
            appointment_detail["end_appointment"] = end_appointment_formatted
            appointment_detail["created_on"] = created_apt_formatted

            reschedule = (
                DateFormatter(full_date=full_date, date=date).documentid_to_datetime(
                    document_id=encrypter
                )
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
                            "back": datetime.datetime.strftime(current_user_date, "%Y-%m-%d"),
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
                            "back": datetime.datetime.strftime(current_user_date, "%Y-%m-%d"),
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
                        "back": datetime.datetime.strftime(current_user_date, "%Y-%m-%d"),
                        "user_check": False,
                    },
                )


def appointment_resched(request, document_id, url_date):
    """Get appointment lists for reschedule.

    Args:
      request: The URL request.
      document_id: document id in firebase firestore
      url_date: for list of appointments on a specific date

    Returns:
        list of appointments
    """
    encrypter = Encrypter(text=document_id).code_decoder()
    current_date = datetime.datetime.strptime(url_date, "%Y-%m-%d")
    full_date = datetime.datetime.now()
    date = datetime.date.today()

    if current_date.date() < datetime.date.today():
        return HttpResponseRedirect(
            reverse(
                "appointment:appointment_resched",
                kwargs={"document_id": document_id, "url_date": datetime.date.today()},
            )
        )

    resched_list = firestoreQuery.resched_appointment(
        year=current_date.year,
        month=current_date.month,
        day=current_date.day,
        hour=23,
        minute=59,
        second=59,
        document_id=encrypter,
        utc_offset=8,
        query_list=["start_appointment", "end_appointment", "created_on"],
    )

    resched_list_rows = firestoreQuery.data_col_row(user_list=resched_list, row=6)

    next_date = current_date + datetime.timedelta(days=1)
    previous_date = current_date - datetime.timedelta(days=1)
    current_date_document = DateFormatter(full_date=full_date, date=date).documentid_to_datetime(
        document_id=encrypter
    )
    return render(
        request,
        "appointment/reschedule.html",
        {
            "current_date": current_date_document.date(),
            "appointment_list": resched_list_rows,
            "next": next_date.date(),
            "previous": previous_date.date(),
            "current": current_date.date(),
            "today": datetime.date.today(),
            "document_id": document_id,
            "curr_year": current_date.year,
            "curr_month": current_date.month - 1,
            "curr_day": current_date.day,
            "is_today": datetime.date.today() == current_date.date(),
        },
    )


def user_resched(request, document_id):
    """Reschedule user's appointment.

    Args:
      request: The URL request.
      document_id: document id in firebase firestore

    Returns:
        None reschedule the user's appointment
    """
    if request.method == "POST":
        full_date = datetime.datetime.now()
        date = full_date.date()
        old_document_id = document_id
        new_document_id = request.POST.get("time")
        decrpyt_document_id = Encrypter(text=new_document_id).code_decoder()
        new_document_datetime = DateFormatter(
            full_date=full_date, date=date
        ).documentid_to_datetime(document_id=decrpyt_document_id)
        new_document_date = new_document_datetime.date()

        old_document_data = firestoreQuery.search_document(
            document_id=old_document_id, collection_name="appointments"
        )

        new_data = firestoreQuery.resched_timedelta(
            data=old_document_data,
            start_appointment=new_document_datetime,
            decrypt_document_id=decrpyt_document_id,
            key_timedelta=["start_appointment", "end_appointment", "created_on"],
            operator="-",
            utc_offset=8,
        )

        # Delete Document Data
        firestoreQuery.delete_document(
            document_id=old_document_id, collection_name="appointments"
        )

        # Add document for reschedule
        firestoreQuery.new_document_data(
            collection_name="appointments", document_id=new_document_id, document_data=new_data
        )

        return HttpResponseRedirect(
            reverse(
                "appointment:appointment_resched",
                kwargs={"document_id": new_document_id, "url_date": new_document_date},
            )
        )

    else:
        return HttpResponseRedirect(
            reverse("appointment:request", kwargs={"document_id": document_id})
        )


def id_verification(request, document_id):
    """Check user ID for verification.IST.

    Args:
      request: The URL request.
      document_id: user appointment document ID

    Returns:
        change document status
    """
    document_id_decrypt = Encrypter(text=document_id).code_decoder()
    date = datetime.date.today()

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
                    full_date=result["created_on"], date=date
                ).date_fb_convert()
                user_results.append(result)

            if len(user_results) != 1 or len(user_results) > 1:
                raise Http404("Data not found.")

            else:
                if len(user_results) == 1:
                    request.session["user_check"] = True
                    request.session["user_verified"] = True
                    request.session["user_list"] = user_results
                    request.session["document_id"] = document_id_decrypt

                    return HttpResponseRedirect(
                        reverse(
                            "appointment:request",
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
                            "appointment:request",
                            kwargs={"document_id": document_id},
                        )
                    )
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
    search_appointment = [firestoreQuery.search_appointment_userid(user_uid=user_uid)]
    date = datetime.date.today()

    user_list = []

    for user in list(search_appointment):
        user["start_appointment"] = DateFormatter(
            full_date=user["start_appointment"], date=date
        ).date_fb_convert()
        user["end_appointment"] = DateFormatter(
            full_date=user["end_appointment"], date=date
        ).date_fb_convert()
        user["created_on"] = DateFormatter(
            full_date=user["created_on"], date=date
        ).date_fb_convert()
        user_list.append(user)

    request.session["user_check"] = True
    request.session["user_verified"] = True
    request.session["user_list"] = user_list
    request.session["document_id"] = search_appointment[0]["document_id"]

    return HttpResponseRedirect(
        reverse(
            "appointment:user_verified",
            kwargs={
                "document_id": Encrypter(text=search_appointment[0]["document_id"]).code_encoder()
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

def document_data(request, document_id, document_name):
    """Get all of the data for the issuing of document.

    Args:
      request: The URL request.
      document_id: document id of appointment
      document_name: name of document

    Returns:
        Renders barangay certificate
    """
    # document_query_data = firestoreQuery.active_document(document_slug=document_name)

    if document_name == "barangay-certificate":
        user_data = firestoreQuery.search_appointment(document_id=document_id)

        check_data = "barangay-certificate" in request.session

        date_today = datetime.date.today()
        current_date = date_today.strftime("%Y-%m-%d")
        validity_date = (date_today + relativedelta(months=+6)).strftime("%Y-%m-%d")

        if check_data:
            active_document_data = firestoreQuery.active_document(document_slug=document_name)

            return render(
                request,
                "appointment/barangay_certificate.html",
                {
                    "document_id": document_id,
                    "document_name": document_name,
                    "user_data": user_data,
                    "current_date": current_date,
                    "validity_date": validity_date,
                    "check_data": check_data,
                    "session_data": request.session["barangay-certificate"] if check_data else "",
                    "document_settings": active_document_data,
                },
            )

        else:
            return render(
                request,
                "appointment/barangay_certificate.html",
                {
                    "document_id": document_id,
                    "document_name": document_name,
                    "user_data": user_data,
                    "current_date": current_date,
                    "validity_date": validity_date,
                    "check_data": check_data,
                    "session_data": request.session["barangay-certificate"] if check_data else "",
                },
            )


def create_document(request, document_id, document_name):
    """Create a document.

    Args:
        request: The URL request.
        document_id: document id of appointment
        document_name: name of document

    Returns:
        document
    """
    if document_name == "barangay-certificate":
        date = request.POST.get("date")
        firstname = request.POST.get("firstname")
        middlename = request.POST.get("middlename")
        lastname = request.POST.get("lastname")
        address = request.POST.get("address")
        year = request.POST.get("year")
        issued_for = request.POST.get("issued")
        conforme = request.POST.get("conforme")
        ctc_no = request.POST.get("ctc_no")
        region = request.POST.get("region")
        or_no = request.POST.get("or_no")
        amount = request.POST.get("amount")
        valid_until = request.POST.get("validity")
        prepared_by = request.POST.get("prepared_by")

        request.session["barangay-certificate"] = {
            "date": date,
            "firstname": firstname,
            "middlename": middlename,
            "lastname": lastname,
            "address": address,
            "year": year,
            "issued_for": issued_for,
            "conforme": conforme,
            "ctc_no": ctc_no,
            "region": region,
            "or_no": or_no,
            "amount": amount,
            "valid_until": valid_until,
            "prepared_by": prepared_by,
        }

        return HttpResponseRedirect(
            reverse(
                "appointment:document_data",
                kwargs={"document_id": document_id, "document_name": document_name},
            )
        )


def remove_document_session(request, date):
    """Remove document session.

    Args:
      request: The URL request.
      date: date of user's appointment

    Returns:
        Removes all of the active session
    """
    for key in list(request.session.keys()):
        del request.session[key]

    return HttpResponseRedirect(reverse("appointment:view_appointments", kwargs={"date": date}))



def get(request, document_id):
    """Notify resident if document is already completed.

    Args:
      request: The URL request.
      document_id: document id of appointment collection in firebase firestore

    Returns:
        sending notification to resident
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
            # user_uid = request.session["user_list"][0]["user_uid"]

            change_docu_status = firestoreQuery.update_appointment_status(
                document_id=document_id, collection_name="appointments"
            )

            if change_docu_status:
                return HttpResponseRedirect(
                    reverse("appointment:process", kwargs={"document_id": document_id})
                )
        else:
            return HttpResponseRedirect(
                reverse("appointment:request", kwargs={"document_id": document_id})
            )


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

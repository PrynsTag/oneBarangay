"""Create your Appointment views here."""
# import base64
import datetime
import logging

import papersize
from dateutil.relativedelta import relativedelta

# Firebase
from django.http import Http404
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from appointment.custom_class.dateformatter import DateFormatter

# from appointment.custom_class.document import Document
from appointment.custom_class.dummy import Dummy
from appointment.custom_class.encrypter import Encrypter
from appointment.custom_class.firestore_data import FirestoreData

from .forms import IdVerification

# from json import dumps


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
                            "document_id": document_id,
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
        # new_document_data_encode = Encrypter(text=new_document_date.__str__()).code_encoder()

        old_document_data = firestoreQuery.search_document(
            document_id=old_document_id, collection_name="appointments"
        )

        new_data = firestoreQuery.resched_timedelta(
            data=old_document_data,
            start_appointment=new_document_datetime,
            new_document_id=new_document_id,
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
                # FIXME: Error created on to resolve add created on in firebase user collection
                result["created_on"] = DateFormatter(
                    full_date=result["creation_date"], date=date
                ).date_fb_convert()

                if result not in user_results:
                    user_results.append(result)

            if len(user_results) == 0:
                raise Http404("Data not found.")
            else:
                # If user is only one
                if len(user_results) == 1:
                    request.session["user_check"] = True
                    request.session["user_verified"] = True
                    request.session["user_list"] = user_results
                    request.session["document_id"] = document_id

                    return HttpResponseRedirect(
                        reverse(
                            "appointment:request",
                            kwargs={"document_id": document_id},
                        )
                    )

                # For multiple users
                elif len(user_results) > 1:
                    request.session["user_check"] = True
                    request.session["user_verified"] = False
                    request.session["document_id"] = document_id
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


def id_verification_manual(request, user_uid, document_id):
    """Verify ID of resident if the account exist.

    Args:
      request: The URL request.
      user_uid: user id in firebase firestore
      document_id:

    Returns:
        session indicating that the user was verified
    """
    search_appointment = firestoreQuery.search_appointment(document_id=document_id)
    search_account = firestoreQuery.search_account_userid(user_uid=user_uid, key="uid")

    for key, value in search_account.items():
        search_appointment[key] = value

    date = datetime.date.today()

    # FIXME: Passing user id rather than appointment document ID

    search_appointment["start_appointment"] = DateFormatter(
        full_date=search_appointment["start_appointment"], date=date
    ).date_fb_convert()
    search_appointment["end_appointment"] = DateFormatter(
        full_date=search_appointment["end_appointment"], date=date
    ).date_fb_convert()
    search_appointment["created_on"] = DateFormatter(
        full_date=search_appointment["created_on"], date=date
    ).date_fb_convert()

    # FIXME: Redirect this to def request then output only the clicked user in table

    request.session["user_check"] = True
    request.session["user_verified"] = True
    request.session["user_list"] = [search_appointment]
    request.session["document_id"] = search_appointment["document_id"]

    return HttpResponseRedirect(
        reverse(
            "appointment:request",
            kwargs={"document_id": document_id},
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
    user_data = firestoreQuery.search_appointment(document_id=document_id)
    issue_status = True

    for document in user_data["document"]:
        if document["ready_issue"]:
            continue
        else:
            issue_status = False
            break

    return render(
        request,
        "appointment/document_process.html",
        {"user_data": user_data, "issue_status": issue_status, "url_date": datetime.date.today()},
    )


def document_data(request, document_id, document_name):
    """Get all of the data for the issuing of document.

    Args:
      request: The URL request.
      document_id: document id of appointment
      document_name: name of document

    Returns:
      : Renders barangay certificate
    """
    # document_query_data = firestoreQuery.active_document(document_slug=document_name)

    if document_name not in ["barangay-certificate", "certificate-of-indigency"]:
        raise Http404("Page not found.")
    elif document_name == "barangay-certificate":
        user_data = firestoreQuery.search_appointment(document_id=document_id)

        check_data = "barangay-certificate" in request.session

        date_today = datetime.date.today()
        current_date = date_today.strftime("%Y-%m-%d")
        validity_date = (date_today + relativedelta(months=+6)).strftime("%Y-%m-%d")

        if check_data:
            active_document_data = firestoreQuery.active_document(document_slug=document_name)

            cert_document_data = request.session["barangay-certificate"]

            document_data_list = []

            for data in active_document_data["document_format"]:
                data["value"] = cert_document_data[data["name"]]
                document_data_list.append(data)

            #     Get document width and length size
            paper_size = papersize.parse_papersize(active_document_data["paper_size"], "mm")

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
                    "session_data": cert_document_data if check_data else "",
                    "document_settings": active_document_data,
                    "document_data": document_data_list,
                    "paper_width": float(paper_size[0]),
                    "paper_length": float(paper_size[1]),
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
    # elif document_name == "certificate-of-indigency":
    #     user_data = firestoreQuery.search_appointment(document_id=document_id)
    #
    #     check_data = "certificate-of-indigency" in request.session
    #
    #     date_today = datetime.date.today()
    #     current_date = date_today.strftime("%Y-%m-%d")
    #     validity_date = (date_today + relativedelta(months=+6)).strftime("%Y-%m-%d")
    #
    #     if check_data:
    #         active_document_data = firestoreQuery.active_document(document_slug=document_name)
    #
    #         document_data = request.session["certificate-of-indigency"]
    #
    #         document_data_list = []
    #
    #         for count, data in enumerate(active_document_data["document_format"]):
    #             data["value"] = document_data[data["name"]]
    #             document_data_list.append(data)
    #
    #         #     Get document width and length size
    #         paper_size = papersize.parse_papersize(active_document_data["paper_size"], "mm")
    #
    #         return render(
    #             request,
    #             "appointment/certificate_of_indigency.html",
    #             {
    #                 "document_id": document_id,
    #                 "document_name": document_name,
    #                 "user_data": user_data,
    #                 "current_date": current_date,
    #                 "validity_date": validity_date,
    #                 "check_data": check_data,
    #                 "session_data": document_data if check_data else "",
    #                 "document_settings": active_document_data,
    #                 "document_data": document_data_list,
    #                 "paper_width": float(paper_size[0]),
    #                 "paper_length": float(paper_size[1]),
    #             },
    #         )
    #
    #     else:
    #         return render(
    #             request,
    #             "appointment/certificate_of_indigency.html",
    #             {
    #                 "document_id": document_id,
    #                 "document_name": document_name,
    #                 "user_data": user_data,
    #                 "current_date": current_date,
    #                 "validity_date": validity_date,
    #                 "check_data": check_data,
    #                 "session_data": request.session["certificate-of-indigency"]
    #                 if check_data
    #                 else "",
    #             },
    #         )


def document_data_edit(request, document_id, document_name):
    """Render edit document.

    Args:
      request: The URL request
      document_id: Document ID of appointment
      document_name: Name of the document in slugify

    Returns:
        View of document
    """
    if document_name not in ["barangay-certificate", "certificate-of-indigency"]:
        raise Http404("Page not found.")

    elif document_name == "barangay-certificate":
        user_data = firestoreQuery.search_appointment(document_id=document_id)

        date_today = datetime.date.today()
        current_date = date_today.strftime("%Y-%m-%d")
        validity_date = (date_today + relativedelta(months=+6)).strftime("%Y-%m-%d")

        active_document_data = firestoreQuery.active_document(document_slug=document_name)

        input_field_data = {}

        for data in user_data["document"]:
            if data["slugify"] == document_name:
                input_field_data = data

        document_data_list = []

        for count, data in enumerate(active_document_data["document_format"]):
            data["value"] = user_data["document"][0][
                active_document_data["document_format"][count]["name"]
            ]
            document_data_list.append(data)

        # Get document width and length size
        paper_size = papersize.parse_papersize(active_document_data["paper_size"], "mm")

        return render(
            request,
            "appointment/barangay_certificate_edit.html",
            {
                "document_id": document_id,
                "document_name": document_name,
                "input_data": input_field_data,
                "user_data": user_data,
                "current_date": current_date,
                "validity_date": validity_date,
                "document_settings": active_document_data,
                "document_data": document_data_list,
                "paper_width": float(paper_size[0]),
                "paper_length": float(paper_size[1]),
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
            "address": address,
            "amount": amount,
            "conforme": conforme,
            "ctc": ctc_no,
            "date": date,
            "firstname": firstname,
            "middlename": middlename,
            "lastname": lastname,
            "fullname": f"{firstname} {middlename} {lastname}",
            "issued": issued_for,
            "orno": or_no,
            "prepared": prepared_by,
            "region": region,
            "valid": valid_until,
            "year": year,
        }

        return HttpResponseRedirect(
            reverse(
                "appointment:document_data",
                kwargs={"document_id": document_id, "document_name": document_name},
            )
        )
    elif document_name == "certificate-of-indigency":
        pass


@csrf_exempt
def confirm_document_data(request, document_id):
    """Update document data.

    Args:
      request: The URL request.
      document_id: Document ID of appointment

    Returns:
        Go to appointment process
    """
    ajax_document_name = request.POST.get("document_name")
    ajax_slugify = request.POST.get("slugify")

    if ajax_slugify == "barangay-certificate":
        date = request.POST.get("date")
        firstname = request.POST.get("firstname")
        middlename = request.POST.get("middlename")
        lastname = request.POST.get("lastname")
        address = request.POST.get("address")
        year = request.POST.get("year")
        issued = request.POST.get("issued")
        conforme = request.POST.get("conforme")
        ctc = request.POST.get("ctc")
        region = request.POST.get("region")
        orno = request.POST.get("orno")
        amount = request.POST.get("amount")
        valid = request.POST.get("valid")
        prepared = request.POST.get("prepared")

        fb_document_data = {
            "document_name": ajax_document_name,
            "slugify": ajax_slugify,
            "date": date,
            "fullname": f"{firstname} {middlename} {lastname}",
            "firstname": firstname,
            "middlename": middlename,
            "lastname": lastname,
            "address": address,
            "year": year,
            "issued": issued,
            "conforme": conforme,
            "ctc": ctc,
            "region": region,
            "orno": orno,
            "amount": amount,
            "valid": valid,
            "prepared": prepared,
            "ready_issue": True,
        }

    final_document_data = []

    final_document_data.append(fb_document_data)

    firestore_document = firestoreQuery.search_appointment(document_id=document_id)
    firestoreQuery.update_document(
        collection_name="appointments",
        document_id=document_id,
        document_data=firestore_document["document"],
        new_document_data=fb_document_data,
        array_name="document",
    )

    return HttpResponse(reverse("appointment:process", kwargs={"document_id": document_id}))


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

def completed(request, document_id):
    """Appointment complete.

    Args:
      request: The URL request.
      document_id: document id of appointment collection in firebase firestore

    Returns:
        None redirect to list of appointments
    """
    full_date = datetime.datetime.now()
    date = full_date.date()

    firestoreQuery.update_appointment_status(
        document_id=document_id, collection_name="appointments"
    )

    date = (
        DateFormatter(full_date=full_date, date=date)
        .documentid_to_datetime(document_id=Encrypter(text=document_id).code_decoder())
        .date()
    )

    return HttpResponseRedirect(reverse("appointment:view_appointments", kwargs={"date": date}))


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


def add_appointment_manual(request, year, month, day):
    """For date testing only.

    Args:
      request: Returns: add date in firestore
      year:
      month:
      day:

    Returns:
        add account in firebase authentication and firestore
    """
    firestore_add_date = Dummy()
    firestore_add_date.add_appointment_account(
        time_interval=15, utc_offset=8, year=year, month=month, day=day
    )

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


def user_verify(request, document_id):
    """Check user existence.

    Args:
      request: The URL request
      document_id: user appointment document ID

    Returns:
        Change user's document status
    """
    if "user_verified" in request.session and "document_id" in request.session:

        session_document_id = request.session["document_id"]

        if session_document_id == document_id:

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


def get_document_resched(request, document_id, url_date):
    """Render issue document reschedule.

    Args:
      request: The URL request
      document_id: Document ID of appointment
      url_date: Date

    Returns:
        Issue document view
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
        "appointment/issue_reschedule.html",
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


def issue_document_resched(request, document_id):
    """Update document data.

    Args:
      request: The URL request
      document_id: Document ID of appointment

    Returns:
        Redirect to page
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
            new_document_id=new_document_id,
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

        firestoreQuery.update_appointment_status(
            document_id=new_document_id, collection_name="appointments"
        )

        return HttpResponseRedirect(
            reverse(
                "appointment:get_document_resched",
                kwargs={"document_id": new_document_id, "url_date": new_document_date},
            )
        )

    else:
        return HttpResponseRedirect(
            reverse("appointment:process", kwargs={"document_id": document_id})
        )

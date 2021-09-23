"""Create your Appointment views here."""
import datetime

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
      : The view_appointment template and the appointments and working hours context data.
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


def details_appointment(request, document_id):
    """Display the details of the user's appointment.

    Args:
      request: The URL request.
      document_id: user appointment document ID

    Returns:
      : renders the html of appointment details
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

            print(f"Start appointment detail formatted: {start_appointment_formatted}")
            print(f"End appointment detail formatted: {end_appointment_formatted}")
            print(
                f"Created On appointment detail formatted: {createdOn_appointment_formatted}"
            )

            if "user_verified" in request.session:

                request.session["user_info"] = appointment_detail

                id_encode = Encrypter(text=document_id).code_encoder()

                return render(
                    request,
                    "appointment/details_appointment.html",
                    {
                        "user_verified": True,
                        "user_detail": appointment_detail,
                        "amount": 100,
                        "form": form,
                        "back": str(datetime.date(year=year, month=month, day=day)),
                        "document_id": id_encode,
                    },
                )
            else:
                return render(
                    request,
                    "appointment/details_appointment.html",
                    {
                        "user_verified": False,
                        "user_detail": appointment_detail,
                        "amount": 100,
                        "form": form,
                        "back": str(datetime.date(year=year, month=month, day=day)),
                    },
                )
        else:
            raise Http404("Invalid Input")


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
    firestore_add_date.add_appointment_account(time_interval=15, utc_offset=8, day=21)

    return HttpResponseRedirect(reverse("services:index"))


def delete_account(request):
    """Delete accounts in authentication and firestore.

    Args:
      request: Returns: delete accounts.

    Returns:
        : delete accounts in firebase authentication and firestore
    """
    firestoreQuery.delete_account_auth()

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

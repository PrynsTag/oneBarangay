"""Create your Appointment views here."""
# Firebase
import datetime
import decimal
import json
import logging
import os

import papersize
import pytz
from dateutil.relativedelta import relativedelta

# from django.core.files.storage import default_storage
# from django.core.files.storage import default_storage
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

# Firestore
# from google.cloud import firestore
from faker import Faker
from firebase_admin import firestore

from appointment.forms import (
    Appointment,
    BarangayCertificate,
    BarangayClearance,
    BarangayIndigency,
    BarangayLocalEmployment,
    BarangayVerification,
    DocumentSelection,
)

# Database
from one_barangay.local_settings import firebase_app

from .custom_class.dummy import Dummy
from .custom_class.firestore_data import FirestoreData

# from datetime import datetime, timedelta


# from firebase_admin.exceptions import AlreadyExistsError


# from collections import OrderedDict


# from operator import getitem


fake = Faker()

# from json import dumps


logger = logging.getLogger(__name__)

firestoreQuery = FirestoreData()

db = firestore.client(firebase_app)

document_list = [
    "barangay-cedula",
    "barangay-certificate",
    "barangay-clearance",
    "barangay-local-employment",
    "barangay-verification",
    "certificate-of-indigency",
]


def request_document(request):
    """Display all available document that can request.

    Args:
      request: URL request

    Returns:
        Request document.
    """
    form = DocumentSelection(request.POST, request.FILES)

    user_sess_data = request.session["user"]

    if request.method == "POST":

        if not form.is_valid():
            raise Http404("error")

        else:
            document = form.cleaned_data["document"]
            purpose = form.cleaned_data["purpose"]
            file = form.cleaned_data["verification"]

            filename = default_storage.generate_filename(file.name)
            default_storage.save(filename, file)
            thumbnail_url = default_storage.url(filename)

            user_sess_data = request.session["user"]
            user_ref = db.collection("users")
            current_user_data = (user_ref.document(user_sess_data["user_id"]).get()).to_dict()
            document_request_ref = db.collection("document_request").document()
            document_request_id = document_request_ref.id

            document_request_list = []

            for data in document:
                admin_settings_document = (
                    db.collection("admin_settings")
                    .document("document")
                    .collection(data)
                    .where("active", "==", True)
                    .stream()
                )

                settings_data = [data.to_dict() for data in admin_settings_document]

                if len(settings_data) == 0 or len(settings_data) > 1:
                    raise Http404("Document settings error.")
                else:
                    data = settings_data[0]
                    document_request_list.append(
                        {
                            "document_name": data["name"],
                            "slugify": data["slugify"],
                            "ready_issue": False,
                            "info_status": False,
                        }
                    )

            request_data = {
                "address": current_user_data["address"],
                "appointment_image": thumbnail_url,
                "appointment_purpose": purpose,
                "contact_number": current_user_data["contact_number"],
                "created_on": datetime.datetime.now(),
                "document_id": document_request_id,
                "email": current_user_data["email"],
                "first_name": current_user_data["first_name"],
                "last_name": current_user_data["last_name"],
                "middle_name": current_user_data["middle_name"],
                "photo_url": current_user_data["photo_url"],
                "role": current_user_data["role"],
                "status": "request",
                "user_id": current_user_data["user_id"],
                "user_verified": False,
                "document": document_request_list,
            }

            document_request_ref.set(request_data)
            user_ref.document(user_sess_data["user_id"]).collection("document_request").document(
                document_request_id
            ).set(request_data, merge=True)

            return HttpResponseRedirect(reverse("services:index"))

    return render(
        request,
        "appointment/request_document.html",
        {"form": form, "user_sess_data": user_sess_data},
    )


def document_request(request):
    """List all document request status in table.

    Args:
      request: URL request

    Returns:
        Render list of user's with request status in table.
    """
    document_ref = db.collection("document_request")

    request_status = document_ref.where("status", "in", ["request", "process"]).stream()
    request_list = [request.to_dict() for request in request_status]

    combine_user_document = []

    for request_data in request_list:
        user_data = db.collection("users").document(request_data["user_id"]).get().to_dict()
        # This code fix if user account was deleted and there is an appointment
        if user_data is None or user_data.get("user_id") is None:
            continue
        else:
            document_temp = []
            for document in request_data["document"]:
                document_temp.append(document["document_name"])

            combine_user_document.append({"document_list": document_temp} | request_data)

    return render(
        request, "appointment/document_request.html", {"request_list": combine_user_document}
    )


def my_document_request(request):
    """Check your document request.

    Args:
      request: URL request

    Returns:
        Display your document request information.
    """
    session_user_data = request.session["user"]

    my_request = (
        db.collection("document_request")
        .where("user_id", "==", session_user_data["user_id"])
        .stream()
    )
    my_request_list = []

    for data in my_request:
        data_dict = data.to_dict()
        document_request_list = []
        for document_data in data_dict["document"]:
            document_request_list.append(document_data["document_name"])
        data_dict["document"] = document_request_list

        my_request_list.append(data_dict)

    return render(
        request,
        "appointment/my_document_request.html",
        {
            "request_data": my_request_list,
            "user_sess_data": session_user_data,
        },
    )


def appointment_schedule(request, document_id):
    """Schedule an appointment.

    Args:
      request: URL request
      document_id: document id in firestore

    Returns:
        Set appointment date and time.
    """
    form = Appointment(request.POST)

    if request.method == "POST":
        if not form.is_valid():

            messages.error(
                request,
                "Invalid appointment.",
            )

            return render(
                request,
                "appointment/appointment_schedule.html",
                {
                    "form": form,
                    "document_id": document_id,
                },
            )

        else:

            start_appointment = form.cleaned_data["date"]
            end_appointment = start_appointment + datetime.timedelta(minutes=15)

            # Document Collection
            document_request_ref = db.collection("document_request")
            document_data = (document_request_ref.document(document_id).get()).to_dict()

            # User Collection
            user_ref = db.collection("users")

            appointment_data = {
                "start_appointment": start_appointment,
                "end_appointment": end_appointment,
            }

            document_request_ref.document(document_id).set(appointment_data, merge=True)
            user_ref.document(document_data["user_id"]).collection("document_request").document(
                document_data["document_id"]
            ).update(appointment_data)

            messages.success(
                request,
                "Appointment Schedule Success",
            )

            return HttpResponseRedirect(reverse("appointment:my_document_request"))

    # office_start = datetime.datetime(
    #     year=datetime.datetime.now().year,
    #     month=datetime.datetime.now().month,
    #     day=datetime.datetime.now().day,
    #     hour=8,
    #     minute=0,
    #     second=0,
    # )
    #
    # office_end = datetime.datetime(
    #     year=datetime.datetime.now().year,
    #     month=datetime.datetime.now().month,
    #     day=datetime.datetime.now().day,
    #     hour=17,
    #     minute=0,
    #     second=0,
    # )
    #
    # temp_time = office_start
    #
    # allowed_times = []
    #
    # appointments = ["08:00", "08:15"]

    # while temp_time.hour != office_end.hour:
    #     allowed_times.append(temp_time.strftime("%H:%M"))
    #     temp_time += datetime.timedelta(minutes=15)

    # filtered_allowed_times = filter(lambda time: time not in appointments, allowed_times)

    return render(
        request,
        "appointment/appointment_schedule.html",
        {
            "form": form,
            "document_id": document_id,
            # "filtered_allowed_times": list(filtered_allowed_times),
        },
    )


def user_document_verification(request, document_id):
    """Display user's document information request.

    Args:
      request: URL request
      document_request_id: document ID in firebase

    Returns:
        Render user document verification view.
    """
    # Document Data
    document_ref = db.collection("document_request")
    user_document_data = document_ref.document(document_id).get().to_dict()

    if user_document_data["user_verified"]:
        return HttpResponseRedirect(
            reverse(
                "appointment:user_issuing_list",
                kwargs={"document_id": user_document_data["document_id"]},
            )
        )

    else:

        # User Collection
        user_ref = db.collection("users")
        user_data = user_ref.document(user_document_data["user_id"]).get().to_dict()

        document_userdata_list = []

        for document in user_document_data["document"]:
            document_userdata_list.append(document["document_name"])

        user_document_data["document_list"] = document_list

        return render(
            request,
            "appointment/user_document_request.html",
            {"document_data": user_document_data, "user_data": user_data},
        )


def user_document_cancel(request, document_id):
    """Remove document request.

    Args:
      request: URL request
      document_request_id: document ID in firebase

    Returns:
        Remove document data in firebase.
    """
    # Document Collection
    document_ref = db.collection("document_request")
    document_data = document_ref.document(document_id).get().to_dict()

    # User Collection
    user_ref = db.collection("users")

    # User document request delete
    user_ref.document(document_data["user_id"]).collection("document_request").document(
        document_data["document_id"]
    ).delete()

    # Document request delete
    document_ref.document(document_data["document_id"]).delete()

    return HttpResponseRedirect(reverse("appointment:document_request"))


def document_request_verified(request, document_request_id):
    """Update document request status.

    Args:
      request: URL request
      document_request_id: document ID in firebase

    Returns:
        Change document status.
    """
    firestoreQuery.update_appointment_status(
        document_id=document_request_id, collection_name="document_request"
    )

    return HttpResponseRedirect(
        reverse(
            "appointment:user_issuing_list",
            kwargs={"document_request_id": document_request_id},
        )
    )


# For User Document Request with Data Table
def user_verification_dt(request, document_id):
    """Render list of users.

    Args:
      request: URL request
      document_request_id: document ID in firebase

    Returns:
        Display list of users.
    """
    verification_status = {"user_verified": True, "status": "process"}

    # Document Collection
    document_ref = db.collection("document_request")
    document_data = document_ref.document(document_id).get().to_dict()
    document_ref.document(document_data["document_id"]).update(verification_status)

    # User Collection
    user_ref = db.collection("users")
    user_ref.document(document_data["user_id"]).collection("document_request").document(
        document_data["document_id"]
    ).update(verification_status)

    return HttpResponseRedirect(
        reverse("appointment:user_issuing_list", kwargs={"document_id": document_id})
    )


def user_selection_data(request, document_request_id):
    """Select user data.

    Args:
      request: URL request
      document_request_id: document ID in firebase

    Returns:
        Change user verified status into true.
    """
    role = {"": 0, "resident": 1, "admin": 2, "worker": 3, "secretary": 4}

    civil_status = {
        "": 0,
        "Single": 1,
        "Married": 2,
        "Widowed": 3,
        "Separated": 4,
        "Divorced": 5,
    }

    if not request.is_ajax():
        raise Http404("Page Not Found.")
    else:
        # json_user_data = json.dumps(request.POST.get("row_data"))
        json_user_data = json.loads(request.POST.get("row_data"))

        json_user_data["Civil Status"] = get_key(
            my_dict=civil_status, val=json_user_data["Civil Status"]
        )
        json_user_data["Role"] = get_key(my_dict=role, val=json_user_data["Role"])

        fb_user_data = (
            db.collection("users")
            .where("first_name", "==", json_user_data["First Name"])
            .where("middle_name", "==", json_user_data["Middle Name"])
            .where("last_name", "==", json_user_data["Last Name"])
            .where("street", "==", json_user_data["Street"])
            .where("role", "==", json_user_data["Role"])
            .where("civil_status", "==", json_user_data["Civil Status"])
        ).stream()

        fb_user_data_list = [data.to_dict() for data in fb_user_data]

        if len(fb_user_data_list) == 0 or len(fb_user_data_list) > 1:
            raise Http404("Account Verification Error")

        # Change status from request to process in document request and user collection
        user_sess_data = request.session["user"]
        document_ref = db.collection("document_request")
        document_ref.document(document_request_id).update(
            {"user_verified": True, "status": "process"}
        )

        send_mail(
            subject="Barangay Malanday - Document Issuing Status",
            message="Your document is in process.",
            from_email=os.getenv("ADMIN_EMAIL"),
            recipient_list=["johnchristianmgaron@gmail.com"],
        )

        user_ref = db.collection("users")
        user_ref.document(user_sess_data["user_id"]).collection("document_request").document(
            document_request_id
        ).update({"user_verified": True, "status": "process"})

        return JsonResponse(
            {
                "success": True,
                "url": reverse(
                    "appointment:user_issuing_list",
                    kwargs={"document_request_id": document_request_id},
                ),
            }
        )


def user_issuing_list(request, document_id):
    """Render user request list of documents.

    Args:
      request: URL request
      document_id: document ID in firebase

    Returns:
        Render document issuing done.
    """
    user_document_data = (db.collection("document_request").document(document_id).get()).to_dict()

    user_data = (db.collection("users").document(user_document_data["user_id"]).get()).to_dict()

    document_list_status = True

    for document_data in user_document_data["document"]:
        if not document_data["ready_issue"]:
            document_list_status = False
            break
        else:
            continue

    return render(
        request,
        "appointment/user_issuing_list.html",
        {
            "user_document_data": user_document_data,
            "user_data": user_data,
            "document_list_status": document_list_status,
        },
    )


def document_issuing_success(request, document_id, document_slugify):
    """Document issuing done.

    Args:
      request: URL request
      document_id: document ID in firebase
      document_slugify: document name in slugify

    Returns:
        Render document issuing done.
    """
    user_document_data = db.collection("document_request").document(document_id.get()).to_dict()
    active_document_settings = (
        db.collection("admin_settings").document(document_slugify).where("active", "==", True)
    ).get()

    active_document_data = [data.to_dict() for data in active_document_settings]

    if len(active_document_data) != 1:
        raise Http404("Document error")

    return render(
        request,
        "appointment/document_issuing_success.html",
        {"user_document_data": user_document_data},
    )


def docu_issue_process(request, document_id, document_slugify):  # noqa: C901
    """Process document issuance.

    Args:
      request: URL request
      document_id: document ID in firebase
      document_slugify: document name in slugify

    Returns:
        Document information.
    """
    user_sess_data = request.session["user"]

    document_settings_ref = db.collection("admin_settings")

    document_settings = (
        document_settings_ref.document("document")
        .collection(document_slugify)
        .where("active", "==", True)
        .get()
    )

    document_settings_data = [data.to_dict() for data in document_settings]

    if len(document_settings_data) != 1:
        raise Http404("Document error.")

    document_settings_data = document_settings_data[0]

    if document_settings is None:
        raise Http404("Page not found.")

    else:
        user_document_data = (
            db.collection("document_request").document(document_id).get()
        ).to_dict()

        for document_data in user_document_data["document"]:
            if document_data["slugify"] == document_slugify:
                if document_data["info_status"]:

                    form = None

                    if document_slugify == "barangay-certificate":
                        form = BarangayCertificate(
                            request.POST or None, initial=document_data["document_data"]
                        )
                    elif document_slugify == "barangay-clearance":
                        form = BarangayClearance(
                            request.POST or None, initial=document_data["document_data"]
                        )
                    elif document_slugify == "barangay-local-employment":
                        form = BarangayLocalEmployment(
                            request.POST or None, initial=document_data["document_data"]
                        )
                    elif document_slugify == "barangay-verification":
                        form = BarangayVerification(
                            request.POST or None, initial=document_data["document_data"]
                        )
                    elif document_slugify == "certificate-of-indigency":
                        form = BarangayIndigency(
                            request.POST or None, initial=document_data["document_data"]
                        )

                    combine_document_list = []

                    for settings_data in document_settings_data["document_format"]:
                        data = document_data["document_data"].get(settings_data["name"])
                        settings_data["value"] = data
                        combine_document_list.append(settings_data)

                    paper_size = papersize.parse_papersize(
                        document_settings_data["paper_size"], "mm"
                    )

                    return render(
                        request,
                        "appointment/docu_issue_process.html",
                        {
                            "form": form,
                            "user_document_data": user_document_data,
                            "document_slugify": document_slugify,
                            "document_info_data": combine_document_list,
                            "document_settings": document_settings_data,
                            "paper_width": float(paper_size[0]),
                            "paper_length": float(paper_size[1]),
                            "info_status": document_data["info_status"],
                        },
                    )
                else:
                    document_validity = (
                        datetime.datetime.now() + relativedelta(months=+3)
                    ).date()
                    first_name = user_document_data["first_name"]
                    middle_name = user_document_data["middle_name"]
                    last_name = user_document_data["last_name"]

                    first_sess_data = user_sess_data["first_name"]
                    middle_sess_data = user_sess_data["middle_name"][0]
                    last_sess_data = user_sess_data["last_name"]

                    initial_dict = {
                        "date": (datetime.datetime.now()).date(),
                        "fullname": f"{first_name} {middle_name} {last_name}",
                        "address": user_document_data["address"],
                        "valid": document_validity,
                        "prepared": f"{first_sess_data} {middle_sess_data}. {last_sess_data}",
                    }

                    form = None

                    if document_slugify == "barangay-certificate":
                        form = BarangayCertificate(request.POST or None, initial=initial_dict)
                    elif document_slugify == "barangay-clearance":
                        form = BarangayClearance(request.POST or None, initial=initial_dict)
                    elif document_slugify == "barangay-local-employment":
                        form = BarangayLocalEmployment(request.POST or None, initial=initial_dict)
                    elif document_slugify == "barangay-verification":
                        form = BarangayVerification(request.POST or None, initial=initial_dict)
                    elif document_slugify == "certificate-of-indigency":
                        form = BarangayIndigency(request.POST or None, initial=initial_dict)

                    return render(
                        request,
                        "appointment/docu_issue_process.html",
                        {
                            "form": form,
                            "user_document_data": user_document_data,
                            "document_slugify": document_slugify,
                            "info_status": document_data["info_status"],
                        },
                    )
            else:
                continue

    return render(
        request,
        "appointment/docu_issue_process.html",
        {
            "document_settings": document_settings_data,
            "user_document_data": user_document_data,
            "document_slugify": document_slugify,
            "ready_issue": False,
        },
    )


def request_update_document(request, document_id, document_slugify):
    """Update request status of document.

    Args:
      request: URL request
      document_request_id: document id in firestore
      document_slugify: document name in slugify

    Returns:
        Change document status in firestore.
    """
    document_request_ref = db.collection("document_request")
    user_docu_data = (document_request_ref.document(document_id).get()).to_dict()

    docu_settings_ref = db.collection("admin_settings")
    docu_settings_data = (
        docu_settings_ref.document("document")
        .collection(document_slugify)
        .where("active", "==", True)
        .get()
    )

    docu_settings_data_list = [data.to_dict() for data in docu_settings_data]

    if len(docu_settings_data_list) == 0 or len(docu_settings_data_list) > 1:
        raise Http404("Document error.")

    else:
        update_docu_data = []

        for docu_data in user_docu_data["document"]:
            if docu_data["slugify"] == document_slugify:
                docu_data["ready_issue"] = True
                docu_data["info_status"] = True
                update_docu_data.append(docu_data)
            else:
                update_docu_data.append(docu_data)

        document_request_ref.document(document_id).update({"document": update_docu_data})
        user_ref = db.collection("users")
        user_ref.document(user_docu_data["user_id"]).collection("document_request").document(
            document_id
        ).update({"document": update_docu_data})

        return HttpResponseRedirect(
            reverse(
                "appointment:user_issuing_list",
                kwargs={"document_id": document_id},
            )
        )


def appointment_update_document(request, document_id, document_slugify):
    """Update appointment document status.

    Args:
      request: URL request
      document_id: document id in firestore
      document_slugify: document name in slugify

    Returns:
        Change document status in firestore.
    """
    #  Document Collection
    document_ref = db.collection("document_request")
    document_data = document_ref.document(document_id).get().to_dict()

    # Document settings collection
    document_settings_ref = db.collection("admin_settings")
    docu_settings_data = (
        document_settings_ref.document("document")
        .collection(document_slugify)
        .where("active", "==", True)
        .get()
    )

    docu_settings_data_list = [data.to_dict() for data in docu_settings_data]

    if len(docu_settings_data_list) == 0 or len(docu_settings_data_list) > 1:
        raise Http404("Document error.")

    else:
        update_docu_data = []

        for docu_data in document_data["document"]:
            if docu_data["slugify"] == document_slugify:
                docu_data["ready_issue"] = True
                docu_data["info_status"] = True
                update_docu_data.append(docu_data)
            else:
                update_docu_data.append(docu_data)

        document_ref.document(document_data["document_id"]).update({"document": update_docu_data})
        user_ref = db.collection("users")
        user_ref.document(document_data["user_id"]).collection("document_request").document(
            document_data["document_id"]
        ).update({"document": update_docu_data})

        return HttpResponseRedirect(
            reverse(
                "appointment:appointment_query_list",
            )
        )


def document_process_change_status(request, document_request_id):
    """Change document status from process to get.

    Args:
      request: URL request
      document_request_id: Document ID

    Returns:
        Update document status in firebase from process to get.
    """
    document_ref = db.collection("document_request")
    document_data = document_ref.document(document_request_id).get().to_dict()
    document_ref.document(document_request_id).update({"status": "get"})

    user_ref = db.collection("users")
    user_ref.document(document_data["user_id"]).collection("document_request").document(
        document_request_id
    ).update({"status": "get"})

    send_mail(
        subject="Barangay Malanday - Document Issuing Status",
        message="You can now get your document.",
        from_email=os.getenv("ADMIN_EMAIL"),
        recipient_list=["johnchristianmgaron@gmail.com"],
    )

    return HttpResponseRedirect(reverse("appointment:document_request"))


def document_input_info(request, document_id, document_slugify):  # noqa: C901
    """Set document information.

    Args:
      request: URL request
      document_id: Document ID
      document_slugify: document name in slugify

    Returns:
        Update document request info in database.
    """
    document_request_ref = db.collection("document_request")
    user_docu_data = (document_request_ref.document(document_id).get()).to_dict()
    user_ref = db.collection("users")

    docu_settings_data = (
        db.collection("admin_settings")
        .document("document")
        .collection(document_slugify)
        .where("active", "==", True)
        .get()
    )
    docu_settings_data_list = [data.to_dict() for data in docu_settings_data]

    if len(docu_settings_data_list) == 0 or len(docu_settings_data_list) > 1:
        raise Http404("Document error.")

    else:
        form_data = {}

        form = None

        if document_slugify == "barangay-certificate":
            form = BarangayCertificate(request.POST)
        elif document_slugify == "barangay-clearance":
            form = BarangayClearance(request.POST)
        elif document_slugify == "barangay-local-employment":
            form = BarangayLocalEmployment(request.POST)
        elif document_slugify == "barangay-verification":
            form = BarangayVerification(request.POST)
        elif document_slugify == "certificate-of-indigency":
            form = BarangayIndigency(request.POST)

        if form.is_valid():
            for data in docu_settings_data[0].get("document_format"):
                if isinstance(form.cleaned_data.get(data["name"]), decimal.Decimal):
                    form_data[data["name"]] = float(form.cleaned_data.get(data["name"]))
                elif isinstance(form.cleaned_data.get(data["name"]), datetime.date):
                    input_date = form.cleaned_data.get(data["name"])
                    form_data[data["name"]] = datetime.datetime(
                        year=input_date.year, month=input_date.month, day=input_date.day
                    )
                else:
                    form_data[data["name"]] = form.cleaned_data.get(data["name"])

            update_docu_data = []

            for docu_data in user_docu_data["document"]:
                if docu_data["slugify"] == document_slugify:
                    docu_data["document_data"] = form_data
                    docu_data["info_status"] = True
                    update_docu_data.append(docu_data)
                else:
                    update_docu_data.append(docu_data)

            document_request_ref.document(document_id).update({"document": update_docu_data})

            user_ref.document(user_docu_data["user_id"]).collection("document_request").document(
                document_id
            ).update({"document": update_docu_data})

            return HttpResponseRedirect(
                reverse(
                    "appointment:docu_issue_process",
                    kwargs={
                        "document_id": document_id,
                        "document_slugify": document_slugify,
                    },
                )
            )


def docu_input_info(request, document_id, document_slugify):  # noqa: C901
    """Set document information.

    Args:
      request: URL request
      document_id: Document ID
      document_slugify: document name in slugify

    Returns:
        Update document request info in database.
    """
    # Document Collection
    document_ref = db.collection("document_request")
    document_data = document_ref.document(document_id).get().to_dict()

    # User Collection
    user_ref = db.collection("users")

    # Admin settings collection
    document_settings_ref = db.collection("admin_settings")
    docu_settings_data = (
        document_settings_ref.document("document")
        .collection(document_slugify)
        .where("active", "==", True)
        .get()
    )
    docu_settings_data_list = [data.to_dict() for data in docu_settings_data]

    if len(docu_settings_data_list) == 0 or len(docu_settings_data_list) > 1:
        raise Http404("Document error.")

    else:
        form_data = {}

        form = None

        if document_slugify == "barangay-certificate":
            form = BarangayCertificate(request.POST)
        elif document_slugify == "barangay-clearance":
            form = BarangayClearance(request.POST)
        elif document_slugify == "barangay-local-employment":
            form = BarangayLocalEmployment(request.POST)
        elif document_slugify == "barangay-verification":
            form = BarangayVerification(request.POST)
        elif document_slugify == "certificate-of-indigency":
            form = BarangayIndigency(request.POST)

        if form.is_valid():
            for data in docu_settings_data[0].get("document_format"):
                if isinstance(form.cleaned_data.get(data["name"]), decimal.Decimal):
                    form_data[data["name"]] = float(form.cleaned_data.get(data["name"]))
                elif isinstance(form.cleaned_data.get(data["name"]), datetime.date):
                    input_date = form.cleaned_data.get(data["name"])
                    form_data[data["name"]] = datetime.datetime(
                        year=input_date.year, month=input_date.month, day=input_date.day
                    )
                else:
                    form_data[data["name"]] = form.cleaned_data.get(data["name"])

            update_docu_data = []

            for docu_data in document_data["document"]:
                if docu_data["slugify"] == document_slugify:
                    docu_data["document_data"] = form_data
                    update_docu_data.append(docu_data)
                else:
                    update_docu_data.append(docu_data)

            document_ref.document(document_data["document_id"]).update(
                {"document": update_docu_data}
            )

            user_ref.document(document_data["user_id"]).collection("document_request").document(
                document_data["document_id"]
            ).update({"document": update_docu_data})

            return HttpResponseRedirect(
                reverse(
                    "appointment:apt_edit_docu",
                    kwargs={
                        "document_id": document_data["document_id"],
                        "document_slugify": document_slugify,
                    },
                )
            )


def add_document_request(request):
    """Add users with appointment.

    Args:
      request: URL request

    Returns:
        Add account in firebase.
    """
    Dummy().add_document_request()
    return HttpResponseRedirect(reverse("services:index"))


def choose_document_request(request, document_request_id):
    """Display user's document request info.

    Args:
      request: URL request
      document_request_id: Document ID

    Returns:
        Render user's document request information.
    """
    request_data = firestoreQuery.get_document_data(
        collection_name="document_request", document_id=document_request_id
    )

    return render(
        request, "appointment/user_document_request.html", {"document_data": request_data}
    )


def appointment_query_list(request):
    """Get all appointment data.

    Args:
      request: URL request

    Returns:
        Display all of appointments.
    """
    # For Appointment Query
    user_sess_data = request.session["user"]

    # Document Collection
    document_ref = db.collection("document_request")

    appointments = None

    if user_sess_data["role"] in ["admin", "head_admin", "secretary", "worker"]:
        appointments = (
            document_ref.where("status", "==", "get")
            .order_by("start_appointment", direction="DESCENDING")
            .stream()
        )
    else:
        appointments = (
            document_ref.where("user_id", "==", user_sess_data["user_id"])
            .where("status", "in", ["get", "complete"])
            .order_by("start_appointment", direction="DESCENDING")
            .stream()
        )

    document_data = [data.to_dict() for data in appointments]

    list_document_data = []

    for data in document_data:
        document_data_list = []

        for document_data in data["document"]:
            document_data_list.append(document_data["document_name"])
        data["document"] = document_data_list

        data["start_appointment"] = data["start_appointment"].astimezone(
            pytz.timezone("Asia/Manila")
        )
        data["end_appointment"] = data["end_appointment"].astimezone(pytz.timezone("Asia/Manila"))

        list_document_data.append(data)

    return render(
        request,
        "appointment/appointment_query_list.html",
        {
            "documents_data": list_document_data,
            "id": "appointment_id",
            "sort": [
                {"sortName": "start_appointment", "sortOrder": "desc"},
            ],
            "user_sess_data": user_sess_data,
        },
    )


def view_appointment(request, document_id):
    """View appointment details.

    Args:
      request: URL request
      document_id: document id in firestore

    Returns:
        Display appointment info.
    """
    # Document Collection
    document_ref = db.collection("document_request")
    document_data = document_ref.document(document_id).get().to_dict()
    document_date = document_data["start_appointment"].date()

    user_sess_data = request.session["user"]

    return render(
        request,
        "appointment/view_appointment.html",
        {
            "document_data": document_data,
            "date": document_date,
            "user_sess_data": user_sess_data,
        },
    )


def view_document_page(request, document_id, document_slugify):
    """View document on another page.

    Args:
      request: URL request
      document_id: document id in firestore
      document_slugify: document name in slugify

    Returns:
        Display a document on another page.
    """
    # Document settings collection
    document_settings_ref = db.collection("admin_settings")
    document_settings = (
        document_settings_ref.document("document")
        .collection(document_slugify)
        .where("active", "==", True)
        .get()
    )

    document_settings_data = [data.to_dict() for data in document_settings]

    if len(document_settings_data) != 1:
        raise Http404("Document error.")

    document_settings_data = document_settings_data[0]

    combine_document_list = []

    # Document Collection
    document_ref = db.collection("document_request")
    user_appointment_data = document_ref.document(document_id).get().to_dict()

    for document_data in user_appointment_data["document"]:
        if document_data["slugify"] == document_slugify:

            combine_document_list = []

            for settings_data in document_settings_data["document_format"]:
                data = document_data["document_data"].get(settings_data["name"])
                settings_data["value"] = data
                combine_document_list.append(settings_data)

            paper_size = papersize.parse_papersize(document_settings_data["paper_size"], "mm")

            return render(
                request,
                "appointment/view_document_page.html",
                {
                    "document_settings": document_settings_data,
                    "document_info_data": combine_document_list,
                    "paper_width": float(paper_size[0]),
                    "paper_length": float(paper_size[1]),
                },
            )


def apt_edit_docu(request, document_id, document_slugify):  # noqa: C901
    """Edit document in appointment.

    Args:
      request: URL request
      document_id: document id in firestore
      document_slugify: document name in slugify

    Returns:
        Change edit document information in appointment.
    """
    document_settings = (
        db.collection("admin_settings")
        .document("document")
        .collection(document_slugify)
        .where("active", "==", True)
        .get()
    )

    document_settings_data = [data.to_dict() for data in document_settings]

    if len(document_settings_data) != 1:
        raise Http404("Document error.")

    document_settings_data = document_settings_data[0]

    if document_settings is None:
        raise Http404("Page not found.")

    else:

        # Document request collection
        document_ref = db.collection("document_request")
        user_document_data = document_ref.document(document_id).get().to_dict()

        for document_data in user_document_data["document"]:
            if document_data["slugify"] == document_slugify:
                if document_data["info_status"]:
                    form = None

                    if document_slugify not in document_list:
                        raise Http404("Page not found.")
                    else:

                        if document_slugify == "barangay-certificate":
                            form = BarangayCertificate(
                                request.POST or None, initial=document_data["document_data"]
                            )
                        elif document_slugify == "barangay-clearance":
                            form = BarangayClearance(
                                request.POST or None, initial=document_data["document_data"]
                            )
                        elif document_slugify == "barangay-local-employment":
                            form = BarangayLocalEmployment(
                                request.POST or None, initial=document_data["document_data"]
                            )
                        elif document_slugify == "barangay-verification":
                            form = BarangayVerification(
                                request.POST or None, initial=document_data["document_data"]
                            )
                        elif document_slugify == "certificate-of-indigency":
                            form = BarangayIndigency(
                                request.POST or None, initial=document_data["document_data"]
                            )

                    combine_document_list = []

                    for settings_data in document_settings_data["document_format"]:
                        if settings_data["name"] == "date":
                            data = document_data["document_data"]["date"].date()
                        elif settings_data["name"] == "valid":
                            data = document_data["document_data"]["valid"].date()
                        else:
                            data = document_data["document_data"].get(settings_data["name"])

                        settings_data["value"] = data
                        combine_document_list.append(settings_data)

                    paper_size = papersize.parse_papersize(
                        document_settings_data["paper_size"], "mm"
                    )

                    return render(
                        request,
                        "appointment/apt_edit_docu.html",
                        {
                            "form": form,
                            "appointment_data": user_document_data,
                            "document_slugify": document_slugify,
                            "document_info_data": combine_document_list,
                            "document_settings": document_settings_data,
                            "paper_width": float(paper_size[0]),
                            "paper_length": float(paper_size[1]),
                            "info_status": document_data["info_status"],
                        },
                    )
                else:
                    document_validity = (
                        datetime.datetime.now() + relativedelta(months=+3)
                    ).date()
                    first_name = document_data["first_name"]
                    middle_name = document_data["middle_name"]
                    last_name = document_data["last_name"]
                    initial_dict = {
                        "date": (datetime.datetime.now()).date(),
                        "fullname": f"{first_name} {middle_name} {last_name}",
                        "address": document_data["address"],
                        "valid": document_validity,
                    }

                    form = None

                    if document_slugify not in document_list:
                        raise Http404("Page not found.")
                    else:

                        form = None

                        if document_slugify == "barangay-certificate":
                            form = BarangayCertificate(request.POST or None, initial=initial_dict)
                        elif document_slugify == "barangay-clearance":
                            form = BarangayClearance(request.POST or None, initial=initial_dict)
                        elif document_slugify == "barangay-local-employment":
                            form = BarangayLocalEmployment(
                                request.POST or None, initial=initial_dict
                            )
                        elif document_slugify == "barangay-verification":
                            form = BarangayVerification(
                                request.POST or None, initial=initial_dict
                            )
                        elif document_slugify == "certificate-of-indigency":
                            form = BarangayIndigency(request.POST or None, initial=initial_dict)

                    return render(
                        request,
                        "appointment/apt_edit_docu.html",
                        {
                            "form": form,
                            "appointment_data": document_data,
                            "document_slugify": document_slugify,
                            "info_status": document_data["info_status"],
                            "date": document_data["start_appointment"].date(),
                        },
                    )
            else:
                continue

    raise Http404("Page not found.")


def reschedule_appointment(request, appointment_id):
    """Reschedule appointment.

    Args:
      request: URL request
      appointment_id: appointment id in firestore

    Returns:
        Reschedule appointment.
    """
    form = Appointment(request.POST)

    # Appointment Collection
    document_ref = db.collection("document_request")
    document_data = document_ref.document(appointment_id).get().to_dict()

    date_url = datetime.date.today()

    if request.method == "POST":

        if not form.is_valid():
            messages.error(
                request,
                "Invalid appointment.",
            )

            return render(
                request,
                "appointment/reschedule_appointment.html",
                {"form": form, "appointment_id": appointment_id, "date": date_url},
            )

        else:

            start_appointment = form.cleaned_data["date"]
            end_appointment = start_appointment + datetime.timedelta(minutes=15)

            document_data_dict = {
                "start_appointment": start_appointment,
                "end_appointment": end_appointment,
            }

            # User Collection
            user_ref = db.collection("users")
            user_ref.document(document_data["user_id"]).collection("document_request").document(
                appointment_id
            ).update(document_data_dict)

            messages.success(
                request,
                "Appointment Schedule Success",
            )

            return HttpResponseRedirect(reverse("appointment:appointment_query_list"))
    else:
        return render(
            request,
            "appointment/reschedule_appointment.html",
            {"form": form, "appointment_id": appointment_id, "date": date_url},
        )


def appointment_complete(request, appointment_id):
    """Appointment complete.

    Args:
      request: URL request
      appointment_id: appointment id in firestore

    Returns:
        Complete appointment.
    """
    status_data = {"status": "complete"}

    # Appointment Collection
    document_ref = db.collection("document_request")
    document_data = document_ref.document(appointment_id).get().to_dict()

    # User Collection
    user_ref = db.collection("users")

    if not document_data["status"] == "get":
        raise Http404("Appointment error.")

    elif document_data["status"] == "get":
        # User Collection
        user_ref.document(document_data["user_id"]).collection("document_request").document(
            document_data["document_id"]
        ).update(status_data)

        # Document request collection
        document_ref.document(appointment_id).update(status_data)

        send_mail(
            subject="Barangay Malanday - Document Issuing Status",
            message="Your document is complete. Thank you!",
            from_email=os.getenv("ADMIN_EMAIL"),
            recipient_list=["johnchristianmgaron@gmail.com"],
        )

        return HttpResponseRedirect(reverse("appointment:appointment_query_list"))


def appointment_cancel(request, document_id):
    """Cancel appointment.

    Args:
      request: URL request
      document_id: document id in firestore

    Returns:
        Remove appointment.
    """
    # Appointment Collection
    document_ref = db.collection("document_request")
    document_data = document_ref.document(document_id).get().to_dict()

    # User Collection
    usr_ref = db.collection("users")
    usr_ref.document(document_data["user_id"]).collection("document_request").document(
        document_data["user_id"]
    ).delete()

    document_ref.document(document_data["document_id"]).delete()

    return HttpResponseRedirect(reverse("appointment:appointment_query_list"))


# Custom Function
# =====================================================

# Get Key Value
def get_key(my_dict: dict, val):
    """Get key value form dictionary using key value.

    Args:
      collection_name: dict: collection in dictionary format
      val: Value in dictionary

    Returns:
        Key from dictionary.
    """
    for key, value in my_dict.items():
        if val == value:
            return key

    return "key doesn't exist"

"""Create your Appointment views here."""
import datetime

# Firebase
import decimal
import json
import logging

import papersize
from dateutil.relativedelta import relativedelta

# from django.core.files.storage import default_storage
# from django.core.files.storage import default_storage
from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

# Firestore
# from google.cloud import firestore
from faker import Faker
from firebase_admin import firestore

from appointment.forms import BarangayCertificate

# Database
from one_barangay.local_settings import firebase_app

from .custom_class.dummy import Dummy
from .custom_class.firestore_data import FirestoreData

# from firebase_admin.exceptions import AlreadyExistsError


# from collections import OrderedDict


# from operator import getitem


fake = Faker()

# from json import dumps


logger = logging.getLogger(__name__)

firestoreQuery = FirestoreData()

db = firestore.client(firebase_app)


def document_request(request):
    """List all document request status in table.

    Args:
      request: URL request

    Returns:
        Render list of user's with request status in table.
    """
    request_status = db.collection("document_request").where("status", "==", "request").get()
    request_list = [request.to_dict() for request in request_status]

    for count, request_data in enumerate(request_list):
        document_temp = []
        for document in request_data["document"]:
            document_temp.append(document["document_name"])

        request_list[count]["document_list"] = document_temp

    return render(request, "appointment/document_request.html", {"request_list": request_list})


def user_document_verification(request, document_request_id):
    """Display user's document information request.

    Args:
      request: URL request
      document_request_id: document ID in firebase

    Returns:
        Render user document verification view.
    """
    user_document_data = (
        db.collection("document_request").document(document_request_id).get()
    ).to_dict()

    if user_document_data["user_verified"]:
        return HttpResponseRedirect(
            reverse(
                "appointment:user_issuing_list",
                kwargs={
                    "document_request_id": user_document_data["document_id"],
                    "user_id": user_document_data["user_uid"],
                },
            )
        )

    else:
        document_list = []

        for document in user_document_data["document"]:
            document_list.append(document["document_name"])

        user_document_data["document_list"] = document_list

        # user_info = db.collection("users").document(user_document_data["user_uid"])

        return render(
            request,
            "appointment/user_document_request.html",
            {"document_data": user_document_data},
        )


def user_document_cancel(request, document_request_id):
    """Remove document request.

    Args:
      request: URL request
      document_request_id: document ID in firebase

    Returns:
        Remove document data in firebase.
    """
    db.collection("document_request").document(document_request_id).delete()

    return HttpResponseRedirect(reverse("appointment:document_request"))


def document_request_verified(request, document_request_id, user_id):
    """Update document request status.

    Args:
      request: URL request
      document_request_id: document ID in firebase
      user_id: user id of user

    Returns:
        Change document status.
    """
    firestoreQuery.update_appointment_status(
        document_id=document_request_id, collection_name="document_request"
    )

    return HttpResponseRedirect(
        reverse(
            "appointment:user_issuing_list",
            kwargs={"document_request_id": document_request_id, "user_id": user_id},
        )
    )


# For User Document Request with Data Table
def user_verification_dt(request, document_request_id):
    """Render list of users.

    Args:
      request: URL request
      document_request_id: document ID in firebase

    Returns:
        Display list of users.
    """
    all_user_data = db.collection("users").stream()

    user_data_list = [user_data.to_dict() for user_data in all_user_data]

    role = {"": 0, "resident": 1, "admin": 2, "worker": 3, "secretary": 4}

    civil_status = {
        "": 0,
        "Single": 1,
        "Married": 2,
        "Widowed": 3,
        "Separated": 4,
        "Divorced": 5,
    }

    keys = ["first_name", "middle_name", "last_name", "street", "role", "civil_status"]
    field = ["First Name", "Middle Name", "Last Name", "Street", "Role", "Civil Status"]

    data_table = []

    for data in user_data_list:
        values_dict = {}

        for count, keys_value in enumerate(keys):
            values_dict[field[count]] = data.get(keys_value)
        data_table.append(values_dict)

    user_data_table = []

    for data in data_table:
        data["Role"] = role.get(data["Role"])
        data["Civil Status"] = civil_status.get(data["Civil Status"])
        user_data_table.append(data)

    return render(
        request,
        "appointment/user_verification_dt.html",
        {"user_data": user_data_table, "document_request_id": document_request_id},
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

        # Change status from request to process
        db.collection("document_request").document(document_request_id).update(
            {"user_verified": True, "status": "process"}
        )

        return JsonResponse(
            {
                "success": True,
                "url": reverse(
                    "appointment:user_issuing_list",
                    kwargs={
                        "document_request_id": document_request_id,
                        "user_id": fb_user_data_list[0].get("user_id"),
                    },
                ),
                "user_data": fb_user_data_list,
            }
        )


def user_filter(request):
    """Search user for verification.

    Args:
      request: URL request

    Returns:
        Verify user document request.
    """
    # role = {"": 0, "resident": 1, "admin": 2, "worker": 3, "secretary": 4}
    #
    # civil_status = {
    #     "": 0,
    #     "Single": 1,
    #     "Married": 2,
    #     "Widowed": 3,
    #     "Separated": 4,
    #     "Divorced": 5,
    # }
    #
    # json_user_data = json.loads(request.POST.get("row_data"))
    #
    # json_user_data["Civil Status"] = get_key(
    #     my_dict=civil_status, val=json_user_data["Civil Status"]
    # )
    # json_user_data["Role"] = get_key(my_dict=role, val=json_user_data["Role"])

    # Image Uploading
    # thumbnail_name = default_storage.get_valid_name(form.cleaned_data["thumbnail"].name)
    # default_storage.save(thumbnail_name, form.cleaned_data["thumbnail"])
    # default_storage.url(filename) # Link
    if request.is_ajax():
        data = json.loads(request.POST.get("data"))
        # print(data)
        return JsonResponse({"data": data})


def user_issuing_list(request, document_request_id, user_id):
    """Render user request list of documents.

    Args:
      request: URL request
      document_request_id: document ID in firebase
      user_id: user id of user

    Returns:
        Render document issuing done.
    """
    user_document_data = (
        db.collection("document_request").document(document_request_id).get()
    ).to_dict()

    user_data = (db.collection("users").document(user_id).get()).to_dict()

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
        {"user_document_dat": user_document_data},
    )


def document_issuing_process(request, document_request_id, document_slugify):
    """Input information in document.

    Args:
      request: URL request
      document_request_id: document ID in firebase
      document_slugify: document name in slugify

    Returns:
        Document information.
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
        raise Http404("Multiple active documents.")

    document_settings_data = document_settings_data[0]

    if document_settings is None:
        raise Http404("Page not found.")

    else:
        user_document_data = (
            db.collection("document_request").document(document_request_id).get()
        ).to_dict()

        if document_slugify == "barangay-certificate":
            for document_data in user_document_data["document"]:
                if document_data["slugify"] == document_slugify:
                    if document_data["ready_issue"]:
                        form = BarangayCertificate(
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
                            "appointment/document_issuing_process.html",
                            {
                                "form": form,
                                "user_document_data": user_document_data,
                                "document_slugify": document_slugify,
                                "document_info_data": combine_document_list,
                                "document_settings": document_settings_data,
                                "paper_width": float(paper_size[0]),
                                "paper_length": float(paper_size[1]),
                                "ready_issue": True,
                            },
                        )
                    else:
                        document_validity = datetime.date.today() + relativedelta(months=+3)
                        first_name = user_document_data["first_name"]
                        middle_name = user_document_data["middle_name"]
                        last_name = user_document_data["last_name"]
                        initial_dict = {
                            "date": datetime.date.today(),
                            "fullname": f"{first_name} {middle_name} {last_name}",
                            "address": user_document_data["address"],
                            "valid": document_validity,
                        }

                        form = BarangayCertificate(request.POST or None, initial=initial_dict)

                        return render(
                            request,
                            "appointment/document_issuing_process.html",
                            {
                                "form": form,
                                "user_document_data": user_document_data,
                                "document_slugify": document_slugify,
                                "ready_issue": False,
                            },
                        )
                else:
                    continue
    return render(
        request,
        "appointment/document_issuing_process.html",
        {
            "document_settings": document_settings_data,
            "user_document_data": user_document_data,
            "document_slugify": document_slugify,
            "ready_issue": False,
        },
    )


def document_process_change_status(request, document_request_id):
    """Change document status from process to get.

    Args:
      request: URL request
      document_request_id: Document ID

    Returns:
        Update document status in firebase from process to get.
    """
    firestoreQuery.update_appointment_status(
        document_id=document_request_id, collection_name="document_request"
    )

    return HttpResponseRedirect(reverse("appointment:document_request"))


def document_input_info(request, document_request_id, document_slugify):
    """Get form value after user submits the document request info.

    Args:
      request: URL request
      document_request_id: Document ID
      document_slugify: document name in slugify

    Returns:
        Update document request info in database.
    """
    document_request_ref = db.collection("document_request")
    user_docu_data = (document_request_ref.document(document_request_id).get()).to_dict()
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
        if document_slugify == "barangay-certificate":
            form = BarangayCertificate(request.POST or None)
            form_data = {}

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
                        docu_data["ready_issue"] = True
                        update_docu_data.append(docu_data)
                    else:
                        update_docu_data.append(docu_data)

                db.collection("document_request").document(document_request_id).update(
                    {"document": update_docu_data}
                )

                return HttpResponseRedirect(
                    reverse(
                        "appointment:document_issuing_process",
                        kwargs={
                            "document_request_id": document_request_id,
                            "document_slugify": document_slugify,
                        },
                    )
                )


def add_document_request(request, account_num):
    """Add users with appointment.

    Args:
      request: URL request
      account_num: Number of accounts

    Returns:
        Add account in firebase.
    """
    Dummy().add_document_request(account_num=account_num)
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


# def view_appointments(request, date):
#     """Display the list of appointments.
#
#     Returns: Display Appointment View
#     """
#     result_dict = None
#     working_hours = [
#         "1300",
#         "0800",
#         "0900",
#         "1000",
#         "1100",
#         "1200",
#         "0700",
#         "1400",
#         "1500",
#         "1600",
#         "1700",
#     ]
#
#     try:
#         # auth.create_user(email="princecarl@gmail.com", password="password123")
#
#         doc_ref = db.collection("appointments").document(
#             (datetime.datetime.now()).strftime("%Y_%m_%d")
#         )
#
#         # View Appointment
#         doc_result = doc_ref.get()
#
#         if not doc_result.exists:
#             raise Http404("No results.")
#         else:
#             result_dict = doc_result.to_dict()
#
#         # Write Appointment Dummy Accounts
#         document = ["Barangay Clearance", "Certificate of Indigency", "Barangay Cedula"]
#
#         status = ["request", "in_progress", "get", "completed"]
#
#         data = {}
#
#         for i in range(700, 1701, 100):
#             collection_id = f"0{str(i)}" if i < 1000 else str(i)
#             apt_id_date = str((datetime.datetime.now()).strftime("%Y_%m_%d"))
#             apt_id_time = str(collection_id)
#             apt_id_number = collection_id[:1]
#
#             data[str(collection_id) if i < 1000 else str(collection_id)] = {
#                 "appointment_id": f"{apt_id_date}{apt_id_time}-{apt_id_number}",
#                 "first_name": fake.first_name(),
#                 "last_name": fake.last_name(),
#                 "document": [document[random.randrange(0, 3)]],
#                 "status": status[random.randrange(0, 4)],
#             }
#
#         doc_ref.set(data)
#     except AlreadyExistsError as already_exist_error:
#         raise Http404 from already_exist_error
#
#     if result_dict is not None:
#         result_dict = OrderedDict(sorted(result_dict.items(), key=lambda x: x))
#
#     return render(
#         request,
#         "appointment/home.html",
#         {"appointments": result_dict, "time_sorted": sorted(working_hours)},
#     )


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

"""Create your Appointment views here."""
import datetime
import random
from collections import OrderedDict
from operator import getitem

# Firebase
import firebase_admin
from django.http import HttpResponse
from django.shortcuts import render
from faker import Faker
# Firestore
# from google.cloud import firestore
from firebase_admin import auth, firestore
from firebase_admin.exceptions import AlreadyExistsError

fake = Faker()


def view_appointment(request):
    """Display the list of appointments.

    Returns: Display Appointment View
    """
    result_dict = None
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

    try:
        # auth.create_user(email="princecarl@gmail.com", password="password123")

        db = firestore.client()
        doc_ref = db.collection(u"appointments").document(
            (datetime.datetime.now()).strftime("%Y_%m_%d")
        )

        # View Appointment
        doc_result = doc_ref.get()

        if doc_result.exists:
            result_dict = doc_result.to_dict()
        else:
            print("There is no result")

        # Write Appointment Dummy Accounts
        # document = ["Barangay Clearance", "Certificate of Indigency", "Barangay Cedula"]
        #
        # status = ["request", "in_progress", "get", "completed"]

        # data = {}

        # for i in range(700, 1701, 100):
        #     collection_id = f"0{str(i)}" if i < 1000 else str(i)
        #
        #     data[str(collection_id) if i < 1000 else str(collection_id)] = {
        #         "appointment_id": '{date}{time}-{number}'.format(
        #             date=str((datetime.datetime.now()).strftime("%Y_%m_%d")),
        #             time=str(collection_id), number=collection_id[:1]
        #         ),
        #         u'first_name': fake.first_name(),
        #         u'last_name': fake.last_name(),
        #         u'document': [document[random.randrange(0, 3)]],
        #         u'status': status[random.randrange(0, 4)]
        #     }

        # doc_ref.set(data)
    except AlreadyExistsError:
        print("Account already exists.")

    if result_dict is not None:
        result_dict = OrderedDict(sorted(result_dict.items(), key=lambda x: x))

    return render(
        request,
        "appointment/home.html",
        {"appointments": result_dict, "time_sorted": sorted(working_hours)},
    )

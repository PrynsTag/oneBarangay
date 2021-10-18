"""Create your Appointment views here."""
import datetime
from collections import OrderedDict
from random import SystemRandom

from django.shortcuts import render
from faker import Faker
from firebase_admin import auth, firestore
from firebase_admin.exceptions import AlreadyExistsError

from one_barangay.local_settings import logger
from one_barangay.scripts.service_account import firestore_auth

fake = Faker()
appointment_app = firestore_auth("appointment_app")
db = firestore.client(appointment_app)

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

account_types = ["admin", "barangay_worker", "resident"]

document = [
    "Barangay Clearance",
    "Certificate of Indigency",
    "Barangay Cedula",
]

status = ["request", "in_progress", "get", "completed"]


def view_appointment(request):
    """Display the list of appointments.

    Returns: renders the view appointment html

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

        # Create Dummy Appointment
        # create_dummy_appointment(num_range=8, doc_ref=doc_ref)

        # Create Dummy Account in Authentication and Firestore
        # create_dummy_account(num_range=10)

        # Create Dummy Account in Authentication and Firestore with Appointment
        # create_dummy_appointment_with_account(num_range=10)

        # Delete Account
        # delete_account_auth()

        # View Appointment
        doc_result = doc_ref.get()

        if doc_result.exists:
            result_dict = doc_result.to_dict()
        else:
            logger.error("There is no result")

    except AlreadyExistsError:
        logger.exception("Account already exists.")

    if result_dict is not None:
        result_dict = OrderedDict(sorted(result_dict.items(), key=lambda x: x))

    return render(
        request,
        "appointment/view_appointment.html",
        {"appointments": result_dict, "time_sorted": sorted(working_hours)},
    )


def details_appointment(request):
    """Display the details of the user's appointment.

    Args:
      request: The URL request.

    Returns:
      Renders the html of appointment details
    """
    return render(request, "appointment/details_appointment.html", {})


def create_dummy_account(num_range: int, password: str):
    """Create dummy account using firebase.

    Args:
      num_range: int:  Number of accounts
      password: str:  default password 'password123'

    Returns:
      returns uid, firstname, lastname, account_type, contact number, email, and password
    """
    crypto_gen = SystemRandom()

    for _ in range(0, num_range):
        first_name = fake.first_name()
        last_name = fake.last_name()
        contact_no = fake.phone_number()
        account_type = account_types[crypto_gen.randrange(0, 3)]
        email = fake.email(domain=None)
        user_uid = None

        doc_ref = db.collection("users").document(f"{account_type}")

        try:
            auth.create_user(email=email, password=password)

        except AlreadyExistsError as e:
            logger.exception("Account already exist. %s", e)

        else:
            user = auth.get_user_by_email(email=email)
            user_uid = user.uid

            data = {
                f"{user_uid}": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "contact_no": contact_no,
                    "user_uid": f"{user_uid}",
                    "account_type": account_type,
                }
            }

            doc_ref.set(data, merge=True)


def create_dummy_appointment_with_account(password: str):
    """Create dummy appointment with account in authentication and firestore.

    Args:
      password: str:  default password 'password123'
    Returns: returns uid, firstname, lastname, account_type, contact number, email, and password
    """
    crypto_gen = SystemRandom()

    for a in range(700, 1701, 100):
        first_name = fake.first_name()
        last_name = fake.last_name()
        contact_no = fake.phone_number()
        account_type = account_types[crypto_gen.randrange(0, 3)]
        email = fake.email(domain=None)
        user_uid = None
        sentence = fake.sentence(nb_words=10)
        image = fake.file_name(category="image", extension="jpeg")
        date = (datetime.datetime.now()).strftime("%Y_%m_%d")
        time = f"0{str(a)}" if a < 1000 else str(a)

        doc_ref_account = db.collection("users").document("resident")

        try:
            auth.create_user(email=email, password=password)

        except AlreadyExistsError:
            logger.exception("Account already exist.")

        else:
            user_uid = (auth.get_user_by_email(email=email)).uid

            data = {
                f"{user_uid}": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "contact_no": contact_no,
                    "user_uid": f"{user_uid}",
                    "account_type": account_type,
                }
            }

            doc_ref_account.set(data, merge=True)

            doc_ref_appointment = db.collection("appointments").document(
                str((datetime.datetime.now()).strftime("%Y_%m_%d"))
            )

            data = {
                (str(time) if a < 1000 else str(time)): {
                    "appointment_id": f"{str(date)}{str(time)}-{time[:1]}",
                    "first_name": first_name,
                    "last_name": last_name,
                    "document": [document[crypto_gen.randrange(0, 3)]],
                    "status": status[crypto_gen.randrange(0, 4)],
                    "user_uid": user_uid,
                    "account_type": account_type,
                    "appointment_date": date,
                    "appointment_time": time,
                    "appointment_purpose": sentence,
                    "appointment_image": image,
                }
            }

            doc_ref_appointment.set(data, merge=True)


def delete_account_auth():
    """Delete all account."""
    doc_ref_account = db.collection("users").document("resident")
    doc_ref_account_result = doc_ref_account.get()

    result_dict = None

    if doc_ref_account_result.exists:
        result_dict = doc_ref_account_result.to_dict()
    else:
        logger.error("There is no result")

    auth.delete_users(list(result_dict))

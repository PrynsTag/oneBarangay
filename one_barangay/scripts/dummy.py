"""Dummy class to generate dummy data."""
import datetime
import logging
from random import SystemRandom

from faker import Faker
from firebase_admin import auth, firestore
from firebase_admin.exceptions import AlreadyExistsError

from one_barangay.scripts.service_account import firestore_auth

appointment_app = firestore_auth("dummy_appointment_app")

logger = logging.getLogger(__name__)

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


class Dummy:
    """Create dummy data."""

    def __init__(self):
        """Initialize Dummy Appointment Properties."""
        self.db = firestore.client(appointment_app)
        self.crypto_gen = SystemRandom()
        self.fake = Faker(["en_PH"])

    def create_dummy_account(self, num_range: int, password: str):
        """Create dummy account using firebase.

        Args:
          num_range: int:  Number of accounts
          password: str:  (Default value = "password123")

        Returns: add dummy accounts in firebase firestore
        """
        for _ in range(0, num_range):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            contact_no = self.fake.phone_number()
            account_type = account_types[self.crypto_gen.randrange(0, 3)]
            email = self.fake.email(domain=None)

            doc_ref = self.db.collection("users").document(f"{account_type}")

            try:
                auth.create_user(email=email, password=password)

            except AlreadyExistsError:
                logger.exception("Account already exist.")

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

    def create_dummy_appointment_with_account(self, password: str):
        """Create dummy appointment with account in authentication and firestore.

        Args:
          password: str:  default password 'password123'
        Returns: adds dummy accounts in firebase authentication and firebase firestore
        """
        for a in range(700, 1701, 100):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            contact_no = self.fake.phone_number()
            account_type = account_types[self.crypto_gen.randrange(0, 3)]
            email = self.fake.email(domain=None)
            sentence = self.fake.sentence(nb_words=10)
            image = self.fake.file_name(category="image", extension="jpeg")
            date = (datetime.datetime.now()).strftime("%Y_%m_%d")
            time = f"0{str(a)}" if a < 1000 else str(a)

            doc_ref_account = self.db.collection("users").document("resident")

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

                doc_ref_appointment = self.db.collection("appointments").document(
                    str((datetime.datetime.now()).strftime("%Y_%m_%d"))
                )

                data = {
                    (str(time) if a < 1000 else str(time)): {
                        "appointment_id": f"{str(date)}_{str(time)}",
                        "first_name": first_name,
                        "last_name": last_name,
                        "document": [document[self.crypto_gen.randrange(0, 3)]],
                        "status": status[self.crypto_gen.randrange(0, 4)],
                        "user_uid": user_uid,
                        "account_type": account_type,
                        "appointment_date": date,
                        "appointment_time": time,
                        "appointment_purpose": sentence,
                        "appointment_image": image,
                    }
                }

                doc_ref_appointment.set(data, merge=True)

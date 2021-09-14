"""Dummy class to generate dummy data."""
import datetime
from random import SystemRandom

from faker import Faker
from firebase_admin import auth, firestore
from firebase_admin.exceptions import AlreadyExistsError

from auth.service_account import firebase_authentication

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

    def create_dummy_account(self, num_range: int, password: str):
        """Create dummy account using firebase.

        Args:
          num_range: int:  Number of accounts
          password: str:  (Default value = "password123")

        Returns: add dummy accounts in firebase firestore
        """
        cryptogen = SystemRandom()
        app = firebase_authentication()
        db = firestore.client(app)
        fake = Faker()

        for _ in range(0, num_range):
            first_name = fake.first_name()
            last_name = fake.last_name()
            contact_no = fake.phone_number()
            account_type = account_types[cryptogen.randrange(0, 3)]
            email = fake.email(domain=None)

            doc_ref = db.collection("users").document(f"{account_type}")

            try:
                auth.create_user(email=email, password=password)

            except AlreadyExistsError:
                print("Account already exist.")

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
        crypto_gen = SystemRandom()
        app = firebase_authentication()
        db = firestore.client(app)
        fake = Faker()

        for a in range(700, 1701, 100):
            first_name = fake.first_name()
            last_name = fake.last_name()
            contact_no = fake.phone_number()
            account_type = account_types[crypto_gen.randrange(0, 3)]
            email = fake.email(domain=None)
            sentence = fake.sentence(nb_words=10)
            image = fake.file_name(category="image", extension="jpeg")
            date = (datetime.datetime.now()).strftime("%Y_%m_%d")
            time = f"0{str(a)}" if a < 1000 else str(a)

            doc_ref_account = db.collection("users").document("resident")

            try:
                auth.create_user(email=email, password=password)

            except AlreadyExistsError:
                print("Account already exist.")

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
                        "appointment_id": "{date}_{time}".format(
                            date=str(date), time=str(time)
                        ),
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

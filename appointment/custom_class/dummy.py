"""Custom class dummy."""
import datetime
import uuid
from random import SystemRandom

from django.http import Http404
from faker import Faker
from firebase_admin import auth, firestore
from firebase_admin.exceptions import AlreadyExistsError
from slugify import slugify

from appointment.custom_class.encrypter import Encrypter
from ocr.scripts import Script
from one_barangay.scripts.service_account import firestore_auth

auth_dummy = firestore_auth(name="dummy_app")

account_types = ["admin", "barangay_worker", "resident"]

document = [
    "Barangay Clearance",
    "Certificate of Indigency",
    "Barangay Cedula",
    "Barangay Certificate",
]

status = ["request", "in_progress", "get", "completed"]

cryptogen = SystemRandom()
fake = Faker()


class Dummy:
    """Create Dummy accounts."""

    def __init__(self):
        """Initialize firebase connection."""
        self.db = firestore.client(auth_dummy)

    # Authentication Account and Firestore User Account
    def create_dummy_account(self, num_range: int, password: str):
        """Create dummy account using firebase.

        Args:
          num_range: int: number of accounts
          password: str: custom password

        Returns:
          add accounts in firebase authentication and firestore
        """
        for _ in range(0, num_range):
            first_name = fake.first_name()
            middle_name = fake.first_name()
            last_name = fake.last_name()
            contact_no = fake.phone_number()
            account_type = account_types[cryptogen.randrange(0, 3)]
            email = fake.email(domain=None)
            user_uid = None

            doc_ref = self.db.collection("users").document(f"{account_type}")

            try:
                auth.create_user(email=email, password=password)

            except AlreadyExistsError as e:
                raise Http404 from e
            else:
                user = auth.get_user_by_email(email=email)
                user_uid = user.uid

                data = {
                    f"{user_uid}": {
                        "first_name": first_name,
                        "middle_name": middle_name,
                        "last_name": last_name,
                        "email": email,
                        "contact_no": contact_no,
                        "user_uid": f"{user_uid}",
                        "account_type": account_type,
                    }
                }

                doc_ref.set(data, merge=True)

    def add_appointment_account(
        self,
        # password: str = "password123",
        year: int = datetime.date.today().year,
        month: int = datetime.date.today().month,
        day: int = datetime.date.today().day,
        time_interval: int = 30,
        time_start: int = 7,
        time_end: int = 17,
        utc_offset: int = 0,
    ):
        """For testing only.

        Args:
          password: str: input default password
          year: int:  (Default value = None)
          month: int:  (Default value = None)
          day: int:  (Default value = None)
          time_interval: int:  (Default value = None) appointment interval in minutes
          time_start: int:  (Default value = None) start of appointment in 24hours (1 -> 01:00am)
          time_end: int:  (Default value = None) end of appointment in 24hours (18 -> 06:00pm)
          utc_offset: int:  (Default value = None) offset for utc

        Returns:
          adds dummy accounts in firebase authentication and appointments in firebase firestore
        """
        doc_ref_appointment = self.db.collection("appointments")
        month = month if 1 > month > 12 else datetime.datetime.now().month

        try:
            datetime.datetime(year=year, month=month, day=day)

        except ValueError as invalid_date:
            raise Http404 from invalid_date

        else:
            temp_hour = time_start
            temp_minute = 0

            count = 1

            while temp_hour < time_end:
                count += 1

                local_datetime = datetime.datetime.strptime(
                    f"{year}-{month}-{day} {temp_hour}:{temp_minute}:{00}",
                    "%Y-%m-%d %H:%M:%S",
                )

                result_utc = local_datetime - datetime.timedelta(hours=utc_offset)

                # For end time of appointment
                f_hour = temp_hour
                f_minute = temp_minute

                if (temp_minute + time_interval) == 60:
                    f_hour += 1
                    f_minute = 0
                else:
                    f_minute = f_minute + time_interval

                local_datetime_adv = datetime.datetime.strptime(
                    f"{year}-{month}-{day} {f_hour}:{f_minute}:{00}",
                    "%Y-%m-%d %H:%M:%S",
                )

                result_utc_adv = local_datetime_adv - datetime.timedelta(hours=8)

                # appointment_id = self.document_id(
                #     year=year, month=month, day=day, hour=temp_hour, minute=temp_minute
                # )
                first_name = fake.first_name()
                middle_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email(domain=None)
                contact_no = fake.phone_number()
                account_type = "resident"
                sentence = fake.sentence(nb_words=10)
                image = fake.file_name(category="image", extension="jpeg")
                try:
                    # Create Account in Firebase Authentication
                    # auth.create_user(email=email, password=password)
                    pass

                except AlreadyExistsError as e:
                    raise Http404 from e

                else:
                    # Get UID on created account in Firebase Authentication
                    # user_uid = auth.get_user_by_email(email=email).uid
                    user_uid = str(uuid.uuid4())

                    doc_ref_account = self.db.collection("users").document(user_uid)

                    # Adding user accounts in firestore
                    user_account_data = {
                        "first_name": first_name,
                        "middle_name": middle_name,
                        "last_name": last_name,
                        "email": email,
                        "contact_no": contact_no,
                        "account_type": account_type,
                        "created_on": str(datetime.datetime.now()),
                        "user_uid": user_uid,
                    }

                    Script().append_to_local_json_file(
                        new_data=user_account_data, filename="dummy"
                    )

                    doc_ref_account.set(user_account_data, merge=True)

                    document_id = self.document_id(
                        year=year,
                        month=month,
                        day=day,
                        hour=temp_hour,
                        minute=temp_minute,
                    )

                    select_document = document[cryptogen.randrange(0, len(document))]

                    # Adding user appointments in firestore
                    appointment_data = {
                        "document_id": Encrypter(text=document_id).code_encoder(),
                        "first_name": first_name,
                        "middle_name": middle_name,
                        "last_name": last_name,
                        "document": [
                            {
                                "document_name": select_document,
                                "slugify": slugify(select_document),
                                "ready_issue": False,
                            }
                        ],
                        "status": status[cryptogen.randrange(0, len(status))],
                        "user_uid": user_uid,
                        "account_type": account_type,
                        "start_appointment": result_utc,
                        "end_appointment": result_utc_adv,
                        "appointment_purpose": sentence,
                        "appointment_image": image,
                        "contact_no": contact_no,
                        "created_on": datetime.datetime.now(),
                    }

                    data_encryptor = Encrypter(text=document_id).code_encoder()

                    doc_ref_appointment.document(data_encryptor).set(appointment_data)

                    if (temp_minute + time_interval) == 60:
                        temp_hour += 1
                        temp_minute = 0
                    else:
                        temp_minute += time_interval

    def add_document_request(self, account_num: int):
        """For testing only.

        Args:
          self: str: input default password
          account_num: int: number of account request

        Returns:
            adds document request
        """
        for _ in range(account_num):

            first_name = fake.first_name()
            middle_name = fake.first_name()
            last_name = fake.last_name()
            address = fake.address()
            email = fake.email(domain=None)
            contact_no = fake.phone_number()
            account_type = "resident"
            sentence = fake.sentence(nb_words=10)
            image = fake.file_name(category="image", extension="jpeg")

            try:
                # Create Account in Firebase Authentication
                # auth.create_user(email=email, password=password)
                pass

            except AlreadyExistsError as e:
                raise Http404 from e

            else:

                # Get UID on created account in Firebase Authentication
                # user_uid = auth.get_user_by_email(email=email).uid
                user_uid = str(uuid.uuid4())

                doc_ref_users = self.db.collection("users").document(user_uid)
                document_request_ref = self.db.collection("document_request").document()
                select_document = document[cryptogen.randrange(0, len(document))]

                # Adding user appointments in firestore
                document_request_data = {
                    "document": [
                        {
                            "document_name": select_document,
                            "slugify": slugify(select_document),
                            "ready_issue": False,
                        }
                    ],
                    # "status": status[cryptogen.randrange(0, len(status))],
                    "status": "request",
                    "user_uid": user_uid,
                    "appointment_purpose": sentence,
                    "appointment_image": image,
                    "created_on": datetime.datetime.now(),
                    "document_id": document_request_ref.id,
                    "user_verified": False,
                }

                document_request_ref.set(document_request_data)

                # Adding user accounts in firestore
                user_account_data = {
                    "first_name": first_name,
                    "middle_name": middle_name,
                    "last_name": last_name,
                    "address": address,
                    "email": email,
                    "contact_no": contact_no,
                    "account_type": account_type,
                    "created_on": str(datetime.datetime.now()),
                    "user_uid": user_uid,
                    "document_request": [document_request_ref.id],
                }

                doc_ref_users.set(user_account_data, merge=True)

    def document_id(self, year: int, month: int, day: int, hour: int, minute: int):
        """Create document ID for firebase firestore document.

        Args:
          year: int: year of document
          month: int: month of document
          day: int: day of document
          hour: int: hour of document
          minute: int: minute of document

        Returns:
          combined year, month, day, hour, and minute in document format
        """
        full_datetime = datetime.datetime(
            year=year, month=month, day=day, hour=hour, minute=minute, second=0
        )

        full_datetime_format = datetime.datetime.strftime(full_datetime, "%Y%m%d-%H%M")

        return full_datetime_format

"""Custom class dummy."""
import datetime
from random import SystemRandom

from faker import Faker
from firebase_admin import auth, firestore
from firebase_admin.exceptions import AlreadyExistsError

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

cryptogen = SystemRandom()
fake = Faker()
db = firestore.client()


class Dummy:
    """Create Dummy accounts."""

    # Authentication Account and Firestore User Account
    def create_dummy_account(self, num_range: int, password: str):
        """Create dummy account using firebase.

        Args:
          num_range: int:  Number of accounts
          password: str:  (Default value = "password123")
        Returns: add dummy accounts in firebase firestore
          num_range: int:
          password: str:
          num_range: int:
          password: str:

        Returns: add accounts in firebase authentication and firestore
        """
        for _ in range(0, num_range):
            first_name = fake.first_name()
            middle_name = fake.first_name()
            last_name = fake.last_name()
            contact_no = fake.phone_number()
            account_type = account_types[cryptogen.randrange(0, 3)]
            email = fake.email(domain=None)
            user_uid = None

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
        password: str = "password123",
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
          : adds dummy accounts in firebase authentication and appointments in firebase firestore
        """
        doc_ref_appointment = db.collection("appointments")
        month = month if 1 > month > 12 else datetime.datetime.now().month

        try:
            datetime.datetime(year=year, month=month, day=day)

        except ValueError:
            day = datetime.datetime.today().day

        finally:
            temp_hour = time_start
            temp_minute = 0

            count = 1

            while temp_hour < time_end:
                print(f"Dummy Count: {count}")
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

                first_name = fake.first_name()
                middle_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email(domain=None)
                contact_no = fake.phone_number()
                account_type = "resident"
                user_uid = None
                sentence = fake.sentence(nb_words=10)
                image = fake.file_name(category="image", extension="jpeg")

                try:
                    # Create Account in Firebase Authentication
                    auth.create_user(email=email, password=password)

                except AlreadyExistsError:
                    print("Account already exist.")

                else:
                    # Get UID on created account in Firebase Authentication
                    user_uid = auth.get_user_by_email(email=email).uid

                    doc_ref_account = db.collection("users").document(user_uid)

                    # Adding user accounts in firestore
                    user_account_data = {
                        "first_name": first_name,
                        "middle_name": middle_name,
                        "last_name": last_name,
                        "email": email,
                        "contact_no": contact_no,
                        "account_type": account_type,
                        "created_on": datetime.datetime.now(),
                    }

                    doc_ref_account.set(user_account_data, merge=True)

                    # Adding user appointments in firestore
                    appointment_data = {
                        "first_name": first_name,
                        "middle_name": middle_name,
                        "last_name": last_name,
                        "document": [document[cryptogen.randrange(0, 3)]],
                        "status": status[cryptogen.randrange(0, 4)],
                        "user_uid": user_uid,
                        "account_type": account_type,
                        "start_appointment": result_utc,
                        "end_appointment": result_utc_adv,
                        "appointment_purpose": sentence,
                        "appointment_image": image,
                        "contact_no": contact_no,
                        "created_on": datetime.datetime.now(),
                    }

                    doc_ref_appointment.add(appointment_data)

                    if (temp_minute + time_interval) == 60:
                        temp_hour += 1
                        temp_minute = 0
                    else:
                        temp_minute += time_interval

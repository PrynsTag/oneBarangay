"""Generate fake user and rbi."""
import csv
import getopt
import json
import sys
from datetime import date, datetime, timedelta
from random import SystemRandom

import pytz
from django.utils.text import slugify
from faker import Faker
from firebase_admin import auth, firestore
from firebase_admin._auth_utils import EmailAlreadyExistsError

from one_barangay.local_settings import logger
from one_barangay.settings import STATIC_URL, firebase_app

firestore_db = firestore.client(app=firebase_app)


class RBI:
    """RBI class."""

    def __init__(self):
        """Initialize RBI attributes."""
        self.fake = Faker(["fil_PH"])
        self.crypto_gen = SystemRandom()

    def create_rbi(self):
        """Create dummy RBI."""
        house_num = str(self.crypto_gen.randrange(100000, 999999))
        address = self.fake.address()
        street = self.crypto_gen.choice(STREET_CHOICES)
        date_accomplished = datetime.combine(
            self.fake.date_between(start_date="-2y"), datetime.min.time()
        )
        last_name = self.fake.last_name()
        creation_date = datetime.now(tz=pytz.timezone("Asia/Manila"))

        family_dictionary = {}
        for idx in range(0, self.crypto_gen.randint(1, 5)):
            first_name = self.fake.first_name()
            middle_name = self.fake.last_name()
            ext = self.fake.suffix()
            birth_place = self.fake.city()
            birth_date = self.fake.date_of_birth(minimum_age=15, maximum_age=60).strftime(
                "%B %d, %Y"
            )

            contact_number = self.fake.mobile_number().replace("-", "")
            formatted_contact_number = (
                contact_number.replace("0", "+63", 1)
                if contact_number.startswith("0")
                else contact_number
            )

            today = date.today()
            birth_date_dt = datetime.strptime(birth_date, "%B %d, %Y")
            age = (
                today.year
                - birth_date_dt.year
                - ((today.month, today.day) < (birth_date_dt.month, birth_date_dt.day))
            )
            civil_status = self.crypto_gen.choice(
                [
                    "Single",
                    "Married",
                    "Divorced",
                    "Widowed",
                    "Separated",
                ]
            )
            citizenship = self.crypto_gen.choice(["Filipino", "Foreigner"])
            if age > 20:
                monthly_income = f"{self.crypto_gen.randrange(1000, 50000):,}"
            else:
                monthly_income = f"{0:,}"

            if idx == 0:
                remarks = "Father"
                sex = "M"
            elif idx == 1:
                remarks = "Mother"
                sex = "F"
            else:
                sex = self.crypto_gen.choice(["M", "F"])
                remarks = self.crypto_gen.choice(["Daughter", "Son"])

            family_dictionary[first_name] = {
                "last_name": last_name,
                "first_name": first_name,
                "middle_name": middle_name,
                "ext": ext,
                "birth_place": birth_place,
                "date_of_birth": birth_date,
                "age": age,
                "sex": sex,
                "contact_number": formatted_contact_number,
                "civil_status": civil_status,
                "citizenship": citizenship,
                "monthly_income": monthly_income,
                "remarks": remarks,
            }

        return {
            "house_data": {
                "house_num": house_num,
                "address": address,
                "street": street,
                "creation_date": creation_date,
                "family_name": last_name,
                "date_accomplished": date_accomplished,
            },
            "family_data": family_dictionary,
        }

    def save_rbi(self, house_data, family_data, user_list_data):
        """Save RBI to firestore rbi collection.

        Args:
          house_data: The house information.
          family_data: The family information.
          user_list_data: The list of users generated from firebase auth.

        Returns:
          None.
        """
        db = firestore.client(app=firebase_app)

        doc_rbi = db.collection("rbi").document(house_data["house_num"])
        for idx, key in enumerate(family_data):
            doc_family = doc_rbi.collection("family").document()
            family_data[key]["member_id"] = doc_family.id

            user_data = {
                "role": user_list_data[idx]["role"],
                "user_id": user_list_data[idx]["user_id"],
                "photo_url": user_list_data[idx]["photo_url"],
                "email": user_list_data[idx]["email"],
            }
            family_auth_data = family_data[key] | user_data

            doc_family.set(family_auth_data, merge=True)

        doc_rbi.set(house_data)


class User:
    """User class."""

    def __init__(self, first_name, last_name):
        """Initialize User attributes."""
        self.firestore_app = firestore.client(app=firebase_app)
        self.fake = Faker(["fil_PH"])
        self.crypto_gen = SystemRandom()

        self.first_name = first_name
        self.last_name = last_name

    def create_user(self):
        """Create dummy user."""
        name_lower = self.first_name.lower()
        email = f"c5zzk.{name_lower}@inbox.testmail.app"
        password = f"{name_lower}123"
        display_name = f"{self.first_name} {self.last_name}"
        role = self.crypto_gen.choice(["resident", "admin", "secretary", "worker", "head_admin"])
        photo_url = f"https://i.pravatar.cc/150?img={self.crypto_gen.randint(1, 70)}"
        phone_number = self.fake.mobile_number().replace("-", "")
        formatted_phone_number = (
            phone_number.replace("0", "+63", 1) if phone_number.startswith("0") else phone_number
        )

        return {
            "email": email,
            "display_name": display_name,
            "photo_url": photo_url,
            "password": password,
            "disabled": False,
            "email_verified": True,
            "phone_number": formatted_phone_number,
            "role": role,
            "app": firebase_app,
        }

    def save_user_to_auth(self, user_data):
        """Save User to firebase auth.

        Args:
          user_data: The user information needed by firebase auth.

        Returns:
          The account information of a user.
        """
        role = user_data.pop("role")

        try:
            user_record = auth.create_user(**user_data)
        except EmailAlreadyExistsError:
            # Generate new email with number appended.
            name = self.first_name + str(self.crypto_gen.randint(0, 99))
            email = f"c5zzk.{name.lower()}@inbox.testmail.app"
            user_data["email"] = email

            user_record = auth.create_user(**user_data)

        auth.set_custom_user_claims(user_record.uid, {role: True}, app=firebase_app)

        return {
            "user_id": user_record.uid,
            "display_name": user_record.display_name,
            "email": user_record.email,
            "role": role,
            "password": user_data["password"],
            "provider": user_record.provider_id,
            "creation_date": user_record.user_metadata.creation_timestamp,
            "last_sign_in": user_record.user_metadata.last_sign_in_timestamp,
            "email_verified": user_record.email_verified,
            "disabled": user_record.disabled,
            "contact_number": user_record.phone_number,
            "photo_url": user_record.photo_url,
        }

    def save_user_to_db(self, auth_data, house_data, family_data, family_member):
        """Save User to firestore collection.

        Args:
          auth_data: The authentication and personal information.
          house_data: The house information of user from RBI.
          family_data: The family information of user from RBI.
          family_member: The member information of user in RBI.
        Returns:
          None.
        """
        auth_data.pop("password")
        auth_information = {
            "contact_number": auth_data["contact_number"],
            "disabled": auth_data["disabled"],
            "email": auth_data["email"],
            "email_verified": auth_data["email_verified"],
            "photo_url": auth_data["photo_url"],
            "role": auth_data["role"],
            "user_id": auth_data["user_id"],
        }
        house_information = {
            "address": house_data["address"],
            "street": house_data["street"],
            "family_name": house_data["family_name"],
        }
        member_information = {
            "citizenship": family_member["citizenship"],
            "civil_status": family_member["civil_status"],
            "date_of_birth": family_member["date_of_birth"],
            "birth_place": family_member["birth_place"],
            "monthly_income": family_member["monthly_income"],
            "middle_name": family_member["middle_name"],
            "first_name": family_member["first_name"],
            "last_name": family_member["last_name"],
            "age": family_member["age"],
            "remarks": family_member["remarks"],
        }
        user_data = auth_information | house_information | member_information

        # Save user data to `users` collection
        doc_user = firestore_db.collection("users").document(auth_data["user_id"])
        doc_user.set(user_data)

        # TODO: https://stackoverflow.com/questions/35187165/python-how-to-subtract-2-dictionaries
        # Save family_data to `family` sub-collection to `user` collection
        # doc_family = doc_user.collection("family").document(auth_data["user_id"])
        for _, member in family_data.items():
            doc_ref = doc_user.collection("family").document()
            doc_ref.set(member | {"member_id": doc_ref.id})

        # Save auth data to `account` sub-collection to `user` collection
        doc_account = doc_user.collection("account").document()
        doc_account.set(auth_data)

    def write_to_csv(self, email, password, role):
        """Write information to csv.

        Args:
          email: The email of the user.
          password: The password of the user.
          role: The role of the user.

        Returns:
          None.
        """
        # Write to CSV File.
        with open("emails.csv", mode="a", encoding="UTF-8") as email_file:
            email_writer = csv.writer(email_file, delimiter=",")
            email_writer.writerow([f"{email}", f"{password}", f"{role}"])


class DocumentRequest:
    """Create dummy document request."""

    def __init__(self):
        """Initialize DocumentRequest properties."""
        self.firestore_app = firestore.client(app=firebase_app)
        self.fake = Faker(["fil_PH"])
        self.crypto_gen = SystemRandom()

    def create_document_request(self, family_member, house_data, auth_data):
        """Create dummy document request.

        Args:
          family_member: the data of the family member.
          house_data: the house information of the user.
          auth_data: the authentication data of user.

        Returns:
          Dictionary data of document request.
        """
        document_type_choices = [
            "Barangay Clearance",
            "Certificate of Indigency",
            "Barangay Cedula",
            "Barangay Certificate",
            "Barangay Local Employment",
            "Barangay Verification",
        ]
        document_type = self.crypto_gen.choice(document_type_choices)
        sentence = self.fake.sentence(nb_words=10)
        appointment_image = STATIC_URL + "assets/img/default-appointment-id.png"

        document_request_data = {
            "document": [
                {
                    "document_name": document_type,
                    "slugify": slugify(document_type),
                    "ready_issue": False,
                    "info_status": False,
                }
            ],
            "status": "request",
            "appointment_purpose": sentence,
            "appointment_image": appointment_image,
            "created_on": datetime.now(tz=pytz.timezone("Asia/Manila")),
            "user_verified": False,
            "first_name": family_member["first_name"],
            "middle_name": family_member["middle_name"],
            "last_name": family_member["last_name"],
            "contact_number": family_member["contact_number"],
            "address": house_data["address"],
            "user_id": auth_data["user_id"],
            "email": auth_data["email"],
            "role": auth_data["role"],
            "photo_url": auth_data["photo_url"],
        }

        return document_request_data

    def save_document_request(self, doc_request_data):
        """Save document request data.

        Args:
          doc_request_data: the data of the request.

        Returns:
          None.
        """
        doc_request_ref = firestore_db.collection("document_request").document()
        doc_req_id = doc_request_ref.id

        doc_request_data.update({"document_id": doc_req_id})

        doc_request_ref.set(doc_request_data, merge=True)

        firestore_db.collection("users").document(doc_request_data["user_id"]).collection(
            "document_request"
        ).document(doc_req_id).set(doc_request_data)


class Complaint:
    """Complaint class."""

    def __init__(self, address, email, name, contact_number, house_num, user_id):
        """Initialize Complaint attributes."""
        self.address = address
        self.email = email
        self.name = name
        self.contact_number = contact_number
        self.house_num = house_num
        self.user_id = user_id

        self.fake = Faker(["fil_PH"])
        self.crypto_gen = SystemRandom()

    def create_complaint(self):
        """Create dummy complaint."""
        date_created = datetime.now(tz=pytz.timezone("Asia/Manila"))
        complaint_type = self.crypto_gen.choice(
            [
                "Gossip Problem",
                "Lending Problem",
                "Obstruction",
                "Public Disturbance",
            ]
        )
        complaint_status = self.crypto_gen.choice(
            ["For Review", "Ongoing", "Handed to Police", "Resolved"]
        )
        comment = self.fake.paragraphs(nb=5)[0]
        image_url = STATIC_URL + "assets/img/default-complaint-image.png"

        return {
            "address": self.address,
            "comment": comment,
            "complainant_name": self.name,
            "complaint_status": complaint_status,
            "complaint_type": complaint_type,
            "contact_number": self.contact_number,
            "date": date_created,
            "email": self.email,
            "house_num": self.house_num,
            "user_id": self.user_id,
            "image_url": image_url,
        }

    def save_complaint(self, complaint_data):
        """Save complaint to firestore complaint and users collection.

        Args:
          complaint_data: The complaint data.

        Returns:
          None.
        """
        db = firestore.client(app=firebase_app)
        doc_ref = db.collection("complaints").document()

        complaint_data["complaint_id"] = doc_ref.id
        doc_ref.set(complaint_data, merge=True)
        (
            db.collection("users")
            .document(complaint_data["user_id"])
            .collection("complaints")
            .document(doc_ref.id)
            .set(complaint_data, merge=True)
        )


class Appointment:
    """Appointment Class."""

    def __init__(self, first_name, last_name, contact_number, user_id, email):
        """Initialize Appointment attributes."""
        self.email = email
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.contact_number = contact_number

        self.fake = Faker(["fil_PH"])
        self.crypto_gen = SystemRandom()

    def create_appointment(self):
        """Create dummy appointment."""
        created_on = datetime.now(tz=pytz.timezone("Asia/Manila"))
        start_appointment = datetime(
            2021,
            11,
            datetime.now(tz=pytz.timezone("Asia/Manila")).day + self.crypto_gen.randint(1, 7),
            self.crypto_gen.randint(0, 23),
            self.crypto_gen.randint(0, 59),
            tzinfo=pytz.timezone("Asia/Manila"),
        )
        end_appointment = start_appointment + timedelta(minutes=15)
        government_id = STATIC_URL + "assets/img/default-appointment-id.png"
        appointment_purpose = self.fake.paragraphs(nb=5)[0]

        document = []
        for _ in range(self.crypto_gen.randint(1, 2)):
            document_type = self.crypto_gen.choice(
                [
                    "indigency",
                    "verification",
                    "local-employment",
                    "cedula",
                    "clearance",
                    "appointment-form",
                    "borrowing-form",
                ]
            )
            document.append(document_type)

        return {
            "appointment": {
                "created_on": created_on,
                "start_appointment": start_appointment,
                "end_appointment": end_appointment,
                "user_id": self.user_id,
                "document": document,
            },
            "appointment_details": {
                "government_id": government_id,
                "appointment_purpose": appointment_purpose,
                "contact_number": self.contact_number,
                "email": self.email,
            },
        }

    def save_appointment(self, appointment_data):
        """Save appointment to firestore user_appointments and users collection.

        Args:
          appointment_data: The appointment information.

        Returns:
          None.
        """
        db = firestore.client(app=firebase_app)

        appointment, appointment_details = (
            appointment_data["appointment"],
            appointment_data["appointment_details"],
        )

        # Save to appointment collection
        doc_appointment = db.collection("user_appointments").document()
        appointment["appointment_id"] = doc_appointment.id
        doc_appointment.set(appointment, merge=True)

        # Save to appointment_details sub-collection
        doc_appointment_details = (
            db.collection("user_appointments")
            .document(doc_appointment.id)
            .collection("appointment_details")
            .document()
        )
        doc_appointment_details.set(appointment_details, merge=True)

        # Save to user collection
        (
            db.collection("users")
            .document(appointment["user_id"])
            .collection("appointments")
            .document(doc_appointment.id)
            .set(appointment, merge=True)
        )


class Announcement:
    """Announcement class."""

    def __init__(self, display_name, user_id):
        """Initialize Announcement attributes."""
        self.display_name = display_name
        self.user_id = user_id

        self.fake = Faker(["fil_PH"])
        self.crypto_gen = SystemRandom()

    def create_announcement(self):
        """Create dummy announcement."""
        body = "\n".join(list(self.fake.paragraphs(nb=5)))
        categories = self.crypto_gen.choice(["covid-19", "political", "environmental"])
        created = datetime.now(tz=pytz.timezone("Asia/Manila"))
        photo_url = STATIC_URL + "assets/img/default-blog-image.jpg"
        thumbnail_name = "default-image"
        title = self.fake.paragraphs(nb=1)[0]
        author = self.display_name
        uid = self.user_id

        return {
            "user_id": uid,
            "author": author,
            "title": title,
            "thumbnail": photo_url,
            "creation_date": created,
            "thumbnail_name": thumbnail_name,
            "featured": self.crypto_gen.choice([True, False]),
            "categories": [categories],
            "body": body,
        }

    def save_announcement(self, announcement_data):
        """Save announcement to firestore announcements and users collection.

        Args:
          announcement_data: The announcement information.

        Returns:
          None.
        """
        db = firestore.client(app=firebase_app)

        announcement_data["announcement_id"] = slugify(announcement_data["title"])
        db.collection("announcements").document(announcement_data["announcement_id"]).set(
            announcement_data, merge=True
        )
        (
            db.collection("users")
            .document(announcement_data["user_id"])
            .collection("announcements")
            .document(announcement_data["announcement_id"])
            .set(announcement_data, merge=True)
        )


def main():
    """Run script."""
    argv = sys.argv[1:]

    try:
        # Define the get opt parameters
        opts, args = getopt.getopt(argv, "n:", ["num_dummy"])
        # Check if the options' length is 1 (can be enhanced)
        if len(opts) == 0 and len(opts) > 1:
            print("usage: generate_dummy_data.py -n <number-of-dummy>")  # noqa: T001
        else:
            _, num_dummy = opts[0]

            for _ in range(int(num_dummy)):
                # RBI Class
                rbi = RBI()
                rbi_data = rbi.create_rbi()
                house_data, family_data = rbi_data["house_data"], rbi_data["family_data"]

                user_list = []
                for _, family_member in family_data.items():
                    # User Class
                    user = User(family_member["first_name"], family_member["last_name"])
                    user_data = user.create_user()
                    auth_data = user.save_user_to_auth(user_data)
                    user.save_user_to_db(auth_data, house_data, family_data, family_member)
                    user.write_to_csv(
                        auth_data["email"], user_data["password"], auth_data["role"]
                    )

                    user_list.append(auth_data)

                    document_request = DocumentRequest()
                    document_request_data = document_request.create_document_request(
                        family_member, house_data, auth_data
                    )
                    document_request.save_document_request(document_request_data)

                    # Complaint Class
                    complaint = Complaint(
                        house_data["address"],
                        auth_data["email"],
                        auth_data["display_name"],
                        auth_data["contact_number"],
                        house_data["house_num"],
                        auth_data["user_id"],
                    )
                    complaint_data = complaint.create_complaint()
                    complaint.save_complaint(complaint_data)

                    # Appointment Class
                    appointment = Appointment(
                        family_member["first_name"],
                        family_member["last_name"],
                        family_member["contact_number"],
                        auth_data["user_id"],
                        auth_data["email"],
                    )
                    appointment_data = appointment.create_appointment()
                    appointment.save_appointment(appointment_data)

                    # Announcement Class
                    announcement = Announcement(
                        auth_data["display_name"],
                        auth_data["user_id"],
                    )
                    announcement_data = announcement.create_announcement()
                    announcement.save_announcement(announcement_data)

                rbi.save_rbi(house_data, family_data, user_list)
                print(  # noqa: T001
                    json.dumps(
                        family_data,
                        indent=4,
                        sort_keys=True,
                        default=str,
                    )
                )

    except getopt.GetoptError:
        # Print something useful
        logger("usage: generate_dummy_data.py -n <number-of-dummy>")
        sys.exit(2)


def delete_all_data():  # noqa: C901
    """Delete all data in firebase."""
    # Firebase Auth
    for user in auth.list_users(app=firebase_app).iterate_all():
        print("------------------ Firebase Auth --------------------")  # noqa: T001
        print("Deleting user " + user.uid)  # noqa: T001
        auth.delete_user(user.uid, app=firebase_app)

    document_request_docs = firestore_db.collection("document_request").stream()
    for doc_request in document_request_docs:
        print("------------------ Document Request --------------------")  # noqa: T001
        print("Deleting document request " + doc_request.id)  # noqa: T001
        doc_request.reference.delete()

    announcement_docs = firestore_db.collection("announcements").stream()
    for post in announcement_docs:
        print("------------------ Announcements --------------------")  # noqa: T001
        print("Deleting post " + post.id)  # noqa: T001
        post.reference.delete()

    appointments_docs = firestore_db.collection("user_appointments").stream()
    for appointment in appointments_docs:
        appointment_details = (
            firestore_db.collection("user_appointments")
            .document(appointment.id)
            .collection("appointment_details")
            .stream()
        )

        for details in appointment_details:
            details.reference.delete()

        print("------------------ Appointments --------------------")  # noqa: T001
        print("Deleting appointment " + appointment.id)  # noqa: T001
        appointment.reference.delete()

    rbi_docs = firestore_db.collection("rbi").stream()
    for rbi in rbi_docs:
        family_docs = (
            firestore_db.collection("rbi").document(rbi.id).collection("family").stream()
        )
        for family in family_docs:
            family.reference.delete()

        print("------------------ RBI --------------------")  # noqa: T001
        print("Deleting rbi " + rbi.id)  # noqa: T001
        rbi.reference.delete()

    complaints_docs = firestore_db.collection("complaints").stream()
    for complaint in complaints_docs:
        print("------------------ Complaint --------------------")  # noqa: T001
        print("Deleting complaint " + complaint.id)  # noqa: T001
        complaint.reference.delete()

    user_ref = firestore_db.collection("users")
    users_docs = user_ref.stream()
    for user in users_docs:
        announcements_user_docs = user_ref.document(user.id).collection("announcements").stream()
        appointments_user_docs = user_ref.document(user.id).collection("appointments").stream()
        complaints_user_docs = user_ref.document(user.id).collection("complaints").stream()
        notification_user_docs = user_ref.document(user.id).collection("notification").stream()
        document_request_user_docs = (
            user_ref.document(user.id).collection("document_request").stream()
        )
        family_user_docs = user_ref.document(user.id).collection("family").stream()
        account_user_docs = user_ref.document(user.id).collection("account").stream()

        for announcement in announcements_user_docs:
            announcement.reference.delete()

        for appointment in appointments_user_docs:
            appointment.reference.delete()

        for complaint in complaints_user_docs:
            complaint.reference.delete()

        for family in family_user_docs:
            family.reference.delete()

        for notification in notification_user_docs:
            notification.reference.delete()

        for document_request in document_request_user_docs:
            document_request.reference.delete()

        for account in account_user_docs:
            account.reference.delete()

        print("------------------ Users --------------------")  # noqa: T001
        print("Deleting user " + user.id)  # noqa: T001
        user.reference.delete()

    # Clear csv file.
    with open("emails.csv", "r+", encoding="UTF-8") as csv_file:
        csv_file.truncate(1)


STREET_CHOICES = [
    "A. Duque",
    "Aca Road",
    "Bangcal Extension",
    "Bartolome Street",
    "C. Molina Street",
    "Central Road",
    "Cherry Blossom Street",
    "Dr. Bartolome",
    "East Road",
    "F. San Diego Street",
    "I. Fernando",
    "I. Lozada Street",
    "Jollibee Drive-Through",
    "M.H. del Pilar Footbridge (footway)",
    "Main Road",
    "North Road",
    "Orange Street",
    "P. Adriano",
    "Peach Street",
    "Road 1",
    "Roseville Street",
    "South RoadSt. Elsewhere Street",
    "T. Santiago Street",
    "West Road",
]

if __name__ == "__main__":
    main()
    # delete_all_data()
    # rbi = RBI()
    # data = rbi.create_rbi()
    # house_data, family_data = data["house_data"], data["family_data"]
    # announcement = Announcement("Prince Velasco", "201812311")
    # data = announcement.create_announcement()
    # data = Appointment(
    #     "Prince",
    #     "Velasco",
    #     "09461653691",
    #     "201812311",
    #     "princevelasco16@gmail.com",
    # ).create_appointment()
    # appointment, appointment_details = data["appointment"], data["appointment_details"]
    # address, email, name, contact_number, house_num, user_id
    # data = Complaint(
    #     "San Mateo",
    #     "princevlasco16@gmail.com",
    #     "Prince",
    #     "09461653691",
    #     "201812311",
    #     "201812311",
    # ).create_complaint()
    #
    # print(  # noqa: T001
    #     json.dumps(
    #         data,
    #         indent=4,
    #         sort_keys=True,
    #         default=str,
    #     )
    # )

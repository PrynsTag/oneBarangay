"""Custom class firestore_data."""
import datetime

from django.shortcuts import Http404
from firebase_admin import firestore


class FirestoreData:
    """Manage firestore data."""

    def __init__(self):
        """Initialize firebase connection."""
        self.db = firestore.client()

    def verify_identification(self, firstname: str, middlename: str, lastname: str):
        """For verification of identification.

        Args:
          firstname: str: user firstname
          middlename: str: user middlename
          lastname: str: user lastname

        Returns:
          : resident information.
        """
        user_list = []

        user_collection = self.db.collection("users")
        query = (
            user_collection.where("first_name", "==", firstname)
            .where("middle_name", "==", middlename)
            .where("last_name", "==", lastname)
        ).stream()

        for info in query:
            user_list.append(info.to_dict())

        return user_list

    def delete_account_auth(self):
        """Delete all account."""
        account_ids = []
        appointment_ids = []
        doc_ref_account = self.db.collection("users")
        doc_ref_appointment = self.db.collection("appointments")

        for result in doc_ref_account.stream():
            account_ids.append(result.id)

            doc_ref_appointment_id = doc_ref_appointment.where(
                "user_uid", "==", result.id
            ).stream()

            for result in doc_ref_appointment_id:
                appointment_ids.append(result.id)

            # auth.delete_users(account_ids)

        for id in account_ids:
            doc_ref_account.document(id).delete()

        for id in appointment_ids:
            doc_ref_appointment.document(id).delete()

    def search_verification(self):
        """Search account for verification."""
        user_ref = self.db.collection("test").where("age", "==", 22).get()

        for res in user_ref:
            print(res.to_dict())

    def day_appointments(
        self, date: datetime.date = datetime.date.today(), utc_offset: int = 0
    ):
        """Get appointment date in firestore.

        You can also manually search the appointment just input the date (year, month, day)

        Args:
          date: datetime.date:  (Default value = datetime.date.today())
          utc_offset: int:  (Default value = 0)

        Returns:
          : get appointment list in firebase firestore
        """
        count = 1
        appointment_list = []

        year = int((str(date)).split(" ")[0].split("-")[0])
        month = int((str(date)).split(" ")[0].split("-")[1])
        day = int((str(date)).split(" ")[0].split("-")[2])

        start_date = datetime.datetime.strptime(
            f"{year}-{month}-{day - 1} {23}:{11}:{59}",
            "%Y-%m-%d %H:%M:%S",
        )

        start_date_delta = start_date - datetime.timedelta(hours=utc_offset)

        end_date = datetime.datetime.strptime(
            f"{year}-{month}-{day} {23}:{11}:{59}", "%Y-%m-%d %H:%M:%S"
        )

        end_date_delta = end_date - datetime.timedelta(hours=utc_offset)

        date_ref = (
            self.db.collection("appointments")
            .where("start_appointment", ">", start_date_delta)
            .where("start_appointment", "<=", end_date_delta)
            .order_by("start_appointment")
        )
        result = date_ref.get()

        for count, appointment in enumerate(result):
            count += 1
            appointment_list.append(appointment.to_dict())

        return count, appointment_list

    def search_appointment(self, document_id: str):
        """Search user appointment.

        Args:
          document_id: str: input user document id

        Returns:
            : user appointment info
        """
        appointment_ref = self.db.collection("appointments")
        user_appointment = appointment_ref.where(
            "document_id", "==", document_id
        ).stream()

        appointment_list = []
        count = 0

        for details in user_appointment:
            appointment_list.append(details.to_dict())
            count += 1

        if count == 1:
            return appointment_list[0]
        else:
            raise Http404("Conflict Appointment ID")

"""Custom class firestore_data."""
import datetime

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

    def query_list(self, search_key: str, value: str):
        """Search user with specific key and value to compare.

        Args:
          search_key: str: key dictionary in firebase firestore data
          value: str: value to be search

        Returns:
          results searched in firebase firestore user collection
        """
        user_list = []
        user_collection = self.db.collection("test_users")
        query = user_collection.where(search_key, "==", value).stream()

        for info in query:
            user_list.append(info.to_dict())

        if len(user_list) != 0:
            return user_list, True
        else:
            return None, False

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
        #
        """
        return self.db.collection("appointments").document(document_id).get().to_dict()

    def search_appointment_userId(self, user_uid: str):
        """Search appointemnt using user uid.

        Args:
          user_uid: str: input user's uid
        Returns:
          : appointment details of user
        """
        appointment_ref = (
            self.db.collection("appointments")
            .where("user_uid", "==", user_uid)
            .stream()
        )

        user_list = []

        for user in appointment_ref:
            user_list.append(user.to_dict())

        if len(user_list) == 1:
            return user_list[0]

    def search_appointment_day(
        self, year: int, month: int, day: int, utc_offset: int = 0
    ):
        """Search appointment using date.

        Args:
          year: int: year of appointment
          month: int: month of appointment
          day: int: day of appointment
          utc_offset: int:  (Default value = 0)
        Returns:
          list of appointments in specific date.
        """
        count = 1

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

        appointment_list = []

        for count, appointment in enumerate(result):
            count += 1
            appointment_list.append(appointment.to_dict())

        return count, appointment_list

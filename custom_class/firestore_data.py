"""Custom class firestore_data."""
import firebase_admin
from firebase_admin import auth, credentials, firestore

from auth.service_account import get_service_from_b64

get_service_from_b64()

db = firestore.client()


class FirestoreData:
    """Firestore account."""

    def verify_identification(self, firstname=None, middlename=None, lastname=None):
        user_collection = db.collection("users")
        query = user_collection.where(
            "resident", "in", ["1dy2QQQGjqYYwJAvHfbxYhr2vnI2"]
        )

        return query

    def delete_account_auth(self):
        """Delete all account."""
        account_ids = []
        appointment_ids = []
        doc_ref_account = db.collection("users")
        doc_ref_appointment = db.collection("appointments")

        for result in doc_ref_account.stream():
            account_ids.append(result.id)

            doc_ref_appointment_id = doc_ref_appointment.where(
                "user_uid", "==", result.id
            ).stream()

            for result in doc_ref_appointment_id:
                appointment_ids.append(result.id)

            auth.delete_users(account_ids)

        for id in account_ids:
            doc_ref_account.document(id).delete()

        for id in appointment_ids:
            doc_ref_appointment.document(id).delete()

    def search_verification(self):
        user_ref = db.collection("test").where("age", "==", 22).get()

        for res in user_ref:
            print(res.to_dict())

    def test_search_date(self):
        import datetime

        start_date = datetime.datetime(year=2021, month=9, day=15, hour=23, minute=59)

        end_date = datetime.datetime(year=2021, month=9, day=16, hour=23, minute=59)

        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")

        date_ref = (
            db.collection("test_appointment")
            .where("start_appointment", ">", start_date)
            .where("end_appointment", "<", end_date)
        )
        result = date_ref.get()

        for count, result in enumerate(result):
            print(f"Count: {count} {result.to_dict()}")

    def day_appointments(
        self, date: datetime.date = datetime.date.today(), utc_offset: int = 0
    ):
        """Get appointment date in firestore.

        You can also manually search the appointment just input the date (year, month, day)

        Args:
          date: datetime.date:  (Default value = datetime.date.today())
          utc_offset: int:  (Default value = 0)
          date: datetime.date:  (Default value = datetime.date.today())
          utc_offset: int:  (Default value = 0)

        Returns:
            : get appointment list in firebase firestore
        """
        import datetime

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
            db.collection("appointments")
            .where("start_appointment", ">", start_date_delta)
            .where("start_appointment", "<=", end_date_delta)
            .order_by("start_appointment")
        )
        result = date_ref.get()

        for count, appointment in enumerate(result):
            count += 1
            appointment_list.append(appointment.to_dict())

        return count, appointment_list

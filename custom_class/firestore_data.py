"""Module for firestore operations."""
import firebase_admin
from firebase_admin import auth, credentials, firestore

from auth.service_account import get_service_from_b64

cred = credentials.Certificate(get_service_from_b64())
default_app = firebase_admin.initialize_app(cred)

db = firestore.client(default_app)


class FirestoreData:
    """Manage firestore data."""

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

"""Module for firestore operations."""
import datetime

from firebase_admin import auth, firestore

from one_barangay.local_settings import logger
from one_barangay.scripts.service_account import firestore_auth

appointment_app = firestore_auth("test_app")


class FirestoreData:
    """Manage firestore data."""

    def __init__(self):
        """Initialize FirestoreData properties."""
        self.db = firestore.client(appointment_app)

    def verify_identification(self):
        """For identification verification.

        Args:
          firstname:  (Default value = None)
          middlename:  (Default value = None)
          lastname:  (Default value = None)

        Returns: data of resident
        """
        user_collection = self.db.collection("users")
        query = user_collection.where("resident", "in", ["1dy2QQQGjqYYwJAvHfbxYhr2vnI2"])

        return query

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

            for appointment_id in doc_ref_appointment_id:
                appointment_ids.append(appointment_id.id)

            auth.delete_users(account_ids)

        for acc_id in account_ids:
            doc_ref_account.document(acc_id).delete()

        for app_id in appointment_ids:
            doc_ref_appointment.document(app_id).delete()

    def search_verification(self):
        """Search age for verification."""
        user_ref = self.db.collection("test").where("age", "==", 22).get()

        for res in user_ref:
            logger.info(res.to_dict())

    def test_search_date(self):
        """Search date for testing only."""
        start_date = datetime.datetime(year=2021, month=9, day=15, hour=23, minute=59)
        end_date = datetime.datetime(year=2021, month=9, day=16, hour=23, minute=59)

        logger.info("Start Date: %s", start_date)
        logger.info("End Date: %s", end_date)

        date_ref = (
            self.db.collection("test_appointment")
            .where("start_appointment", ">", start_date)
            .where("end_appointment", "<", end_date)
        )
        result = date_ref.get()

        for count, result in enumerate(result):
            logger.info("Count: %s %s", count, result.to_dict())

"""Module for firestore operations."""
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore

from auth.service_account import get_service_from_b64

cred = credentials.Certificate(get_service_from_b64())
default_app = firebase_admin.initialize_app(cred)

db = firestore.client(default_app)


class FirestoreData:
    """Manage firestore data."""

    def delete_account_auth(self):
        """Delete all account."""
        doc_ref_account = db.collection("users").document("resident")
        doc_ref_account_result = doc_ref_account.get()

        result_dict = None

        if doc_ref_account_result.exists:
            result_dict = doc_ref_account_result.to_dict()
        else:
            print("There is no result(s)")

        auth.delete_users(list(result_dict))

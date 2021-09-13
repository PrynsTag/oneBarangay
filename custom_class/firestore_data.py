from firebase_admin import auth, firestore
from auth.service_account import firebase_authentication

app = firebase_authentication()
db = firestore.client(app)


class FirestoreData:
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

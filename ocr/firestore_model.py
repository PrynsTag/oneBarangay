"""Database query in Firestore for OCR."""
import json
import os

import requests
from firebase_admin import firestore

from ocr.dummy_data import RBIDummy
from ocr.scripts import Script
from one_barangay.scripts.service_account import firestore_auth

firestore_app = firestore_auth()


class FirestoreModel:
    """Firestore OCR Model Class."""

    def __init__(self):
        """Initialize class variables."""
        self.db = firestore.client(firestore_app)
        self.doc_ref_rbi = self.db.collection("rbi")
        self.script = Script()
        self.dummy = RBIDummy()

    def get_rbi(self):
        """First paginated query."""
        if os.getenv("GAE_ENV", "").startswith("standard"):
            formatted_data = json.loads(
                requests.get(
                    "https://onebaragay.blob.core.windows.net/json-data/rbi_data.json"
                ).text
            )
        else:
            doc_ref_limit = self.doc_ref_rbi.order_by("created_at", direction="DESCENDING")
            family_document_list = [doc.to_dict() for doc in doc_ref_limit.get()]
            formatted_data = self.script.format_firestore_data(family_document_list)

        return formatted_data

    def store_rbi(self, data):
        """Store RBI document in firestore.

        Args:
          data: The data to be stored.

        Returns:
          None.
        """
        doc_ref_house_num = self.doc_ref_rbi.document(str(data["house_num"]))
        doc_ref_house_num.set(data, merge=True)

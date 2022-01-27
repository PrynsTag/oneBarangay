"""Database query in Firestore for OCR."""
import json
import os

import requests
from firebase_admin import firestore
from google.api_core.exceptions import NotFound

from ocr.dummy_data import RBIDummy
from ocr.scripts import Script
from one_barangay.local_settings import logger
from one_barangay.scripts.service_account import firestore_auth

firestore_app = firestore_auth("ocr_app")


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
                requests.get("https://onebaragay.blob.core.windows.net/json-data/rbi_data.json").text
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

    def get_resident_rbi(self, user_data) -> dict:
        """Get the residents RBI.

        Args:
          user_data: The data of the user to search for.

        Returns:
          The data dictionary of the user.
        """
        try:
            doc = (
                self.doc_ref_rbi.where(
                    f"family_members.{user_data['first_name']}.last_name",
                    "==",
                    user_data["last_name"],
                )
                .limit(1)
                .get()[0]
            ).to_dict()
            resident_data = doc["family_members"][user_data["first_name"]]
            resident_data["address"] = doc["address"]
            resident_data["house_num"] = doc["house_num"]

            return resident_data
        except IndexError as e:
            logger.exception("User not found. %s", e)
            return {}
        except NotFound as e:
            logger.exception("User not found. %s", e)
            return {}
        except TypeError as e:
            logger.exception("Something went wrong. %s", e)
            raise TypeError(f"Something went wrong. {e}") from e

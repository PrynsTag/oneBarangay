"""Database query in Firestore for OCR."""

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

    def rbi_current_page(self):
        """First paginated query."""
        doc_ref_limit = self.doc_ref_rbi.order_by("created_at", direction="DESCENDING").limit(3)
        family_document_list = [doc.to_dict() for doc in doc_ref_limit.get()]
        formatted_data = self.script.format_firestore_data(family_document_list)

        self.script.write_to_json(formatted_data)

        return formatted_data

    def rbi_next_page(self, created_at):
        """Next pagination query.

        Args:
          created_at:

        Returns:
          : The next query after the parameter `created_at`.
        """
        next_page_query = (
            self.doc_ref_rbi.order_by("created_at", direction="DESCENDING")
            .start_after({"created_at": created_at})
            .limit(3)
        )

        doc_id_list = [doc.id for doc in next_page_query.stream()]

        family_document_list = [
            self.db.collection("rbi").document(f"{doc_id}").get().to_dict()
            for doc_id in doc_id_list
        ]

        formatted_data = self.script.format_firestore_data(family_document_list)

        return formatted_data

    def rbi_previous_page(self, created_at):
        """Previous pagination query.

        Args:
          created_at:

        Returns:
          : The previous query before the parameter `created_at`.
        """
        previous_page_query = (
            self.doc_ref_rbi.order_by("created_at", direction="DESCENDING")
            .end_before({"created_at": created_at})
            .limit_to_last(3)
        )

        doc_id_list = [col.id for col in previous_page_query.get()]

        family_document_list = [
            self.db.collection("rbi").document(f"{doc_id}").get().to_dict()
            for doc_id in doc_id_list
        ]

        formatted_data = self.script.format_firestore_data(family_document_list)

        return formatted_data

    def store_dummy_rbi(self):
        """Store dummy RBI."""
        dummy_data = self.dummy.create_rbi()
        doc_ref_house_num = self.doc_ref_rbi.document(dummy_data["house_num"])
        doc_ref_house_num.set(dummy_data, merge=True)

    def store_rbi(self, house_num, data):
        """Store RBI document in firestore.

        Args:
          house_num: The house number of the RBI document.
          data: The data to be stored.

        Returns:
          None.
        """
        doc_ref_house_num = self.doc_ref_rbi.document(house_num)
        doc_ref_house_num.set(data, merge=True)

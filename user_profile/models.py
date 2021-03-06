"""Create your models here."""

from firebase_admin import firestore
from google.api_core.exceptions import NotFound

from one_barangay.local_settings import logger
from one_barangay.settings import firebase_app


class UserModel:
    """Class for Firestore User Collection."""

    def __init__(self):
        """Initialize UserModel attributes."""
        self.db = firestore.client(app=firebase_app)
        self.user_ref = self.db.collection("users")

    def get_user_data(self, user_id: str) -> dict:
        """Get user data from firestore.

        Args:
          user_id: The user id to fetch.

        Returns:
          The dictionary data of user or empty.
        """
        # try:
        user_data = self.user_ref.document(user_id).get().to_dict()
        try:
            if user_data.get("updated_on"):
                user_data["updated_on"] = user_data["updated_on"].strftime("%B %d, %Y, %H:%M:%S")
            else:
                logger.exception("[UserModel.get_user_data] User updated_on key not found.")
                return user_data
        except KeyError:
            logger.exception("[UserModel.get_user_data] No timestamp key..")
            return user_data
        except NotFound as e:
            logger.exception("[UserModel.get_user_data] User not found. %s", e)
            return {}
        except TypeError as e:
            logger.exception("[UserModel.get_user_data] User account retrieval failed. %s", e)
            return {}

        return user_data

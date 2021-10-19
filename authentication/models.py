"""Create your authentication models here."""
from firebase_admin import firestore
from google.api_core.exceptions import NotFound

from one_barangay.local_settings import logger
from one_barangay.settings import firebase_app


class AuthModel:
    """Class for firestore authentication database."""

    def __init__(self):
        """Initialize AuthModel attributes."""
        self.db = firestore.client(app=firebase_app)
        self.rbi_ref = self.db.collection("rbi")
        self.user_ref = self.db.collection("users")

    def connect_data_to_rbi(self, user_data: dict) -> bool:
        """Associate authentication and rbi data.

        Args:
          user_data: The data of the user.

        Returns:
          Boolean True if the rbi of authenticated user exists, False if not.
        """
        try:
            doc = (
                self.rbi_ref.where(
                    f"family_members.{user_data['first_name']}.last_name",
                    "==",
                    user_data["last_name"],
                )
                .limit(1)
                .get()[0]
            )

            if doc.exists:
                self.rbi_ref.document(doc.id).update(
                    {
                        f"family_members.{user_data['first_name']}.uid": user_data["uid"],
                        f"family_members.{user_data['first_name']}.email": user_data["email"],
                        f"family_members.{user_data['first_name']}.photo": user_data["photo"]
                        if user_data.get("photo")
                        else user_data.get("photo_url"),
                        f"family_members.{user_data['first_name']}.phone_number": user_data[
                            "phone_number"
                        ],
                    }
                )
                logger.info(
                    "[AuthModel.connect_auth_to_rbi] User %s created in rbi collection.",
                    user_data["uid"],
                )
                return True
            else:
                logger.warning(
                    "[AuthModel.connect_auth_to_rbi] User %s NOT in rbi collection.",
                    user_data["uid"],
                )
                return False
        except IndexError as e:
            logger.exception(
                "[AuthModel.connect_auth_to_rbi] User %s not found in rbi collection. %s",
                user_data["uid"],
                e,
            )
            return False
        except NotFound as e:
            logger.exception(
                "[AuthModel.connect_auth_to_rbi] User %s not found in rbi collection. %s",
                user_data["uid"],
                e,
            )
            return False
        except TypeError as e:
            logger.exception("Something went wrong. %s", e)
            raise TypeError("Something went wrong.") from e

    def store_user_data(self, uid: str, user_data: dict) -> bool:
        """Store user data in users collection.

        Args:
          uid: The user id of the authenticated user.
          user_data: The data of the authenticated user.

        Returns:
          None.
        """
        try:
            user_data["timestamp"] = firestore.SERVER_TIMESTAMP
            self.user_ref.document(uid).set(user_data, merge=True)
            logger.info(
                "[AuthModel.store_user_data] User %s created in firestore users collection.", uid
            )
            return True
        except IndexError as e:
            logger.exception("[AuthModel.store_user_data] User %s not created. %s", uid, e)
            return False
        except NotFound as e:
            logger.exception("[AuthModel.store_user_data] User %s not created. %s", uid, e)
            return False
        except TypeError as e:
            logger.exception("[AuthModel.store_user_data] Something went wrong. %s", e)
            raise TypeError("[AuthModel.store_user_data] Something went wrong.") from e

    def update_user_data(self, uid: str, user_data: dict) -> bool:
        """Update user data from firestore users collection.

        Args:
          uid: The user id of the authenticated user.
          user_data: The data of the authenticated user.

        Returns:
          None.
        """
        try:
            user_data["timestamp"] = firestore.SERVER_TIMESTAMP
            self.user_ref.document(uid).update(user_data)
            return True
        except NotFound as e:
            logger.exception("User Not Found. %s", e)
            return False
        except TypeError as e:
            logger.exception("Something went wrong. %s", e)
            return False

"""Create your models here."""
import os
import uuid
from datetime import datetime
from typing import Any

import pytz
from django.core.mail import send_mail
from firebase_admin import auth, firestore
from firebase_admin._auth_utils import UserNotFoundError
from firebase_admin.auth import UserRecord

from authentication.models import AuthModel
from ocr.firestore_model import FirestoreModel
from one_barangay.local_settings import logger
from one_barangay.scripts.storage_backends import AzureStorageBlob
from one_barangay.settings import firebase_app
from user_management.json_functions import UserManagementJSON


class FirebaseAuth:
    """Class for working with Firebase Auth."""

    def __init__(self):
        """Initialize FirebaseAuth attributes."""
        self.json = UserManagementJSON("auth_data.json")

    def get_all_user(self) -> list[dict[str, Any]]:
        """Retrieve all user from Firebase Auth."""
        all_users = [
            {
                "uid": user.uid,
                "display_name": user.display_name,
                "email": user.email,
                "role": "".join([*user.custom_claims]),
                "provider": user.provider_id,
                "creation_date": user.user_metadata.creation_timestamp,
                "last_sign_in": user.user_metadata.last_sign_in_timestamp,
                "email_verified": user.email_verified,
                "disabled": user.disabled,
                "phone_number": user.phone_number,
                "photo_url": user.photo_url,
            }
            for user in auth.list_users(app=firebase_app).iterate_all()
        ]

        return all_users

    def add_user(self, user_info: dict) -> None:
        """Add a user to Firebase Auth.

        Args:
          user_info: Dict: The information of user to be added.

        Returns:
          None.
        """
        auth_data = {}
        user = UserRecord(None)
        if os.getenv("GAE_ENV", "").startswith("standard"):
            role = user_info.pop("role")
            # firebase_admin._auth_utils.EmailAlreadyExistsError
            # Create user in Firebase Auth with Custom Claim.
            user_info["app"] = firebase_app
            user = auth.create_user(**user_info)
            auth.set_custom_user_claims(user.uid, {role: True}, app=firebase_app)

            # Get Firebase Auth and Resident (RBI) Data from Firestore
            user = auth.get_user(user.uid, app=firebase_app)
            first_name, last_name = user.display_name.split()
            auth_data = {
                "uid": user.uid,
                "display_name": user.display_name,
                "first_name": first_name,
                "last_name": last_name,
                "email": user.email,
                "role": "".join([*user.custom_claims]),
                "provider": user.provider_id,
                "creation_date": user.user_metadata.creation_timestamp,
                "last_sign_in": user.user_metadata.last_sign_in_timestamp,
                "email_verified": user.email_verified,
                "disabled": user.disabled,
                "phone_number": user.phone_number,
                "photo_url": user.photo_url,
            }
            resident_data = FirestoreModel().get_resident_rbi(auth_data)
            auth_and_resident_data = auth_data | resident_data

            # Add new user to firestore rbi collection.
            auth_model = AuthModel()
            # TODO: Use modal to ask additional info.
            auth_model.connect_data_to_rbi(auth_and_resident_data)

            # Store Firebase Auth and Resident (RBI) Data to firestore `users` collection.
            auth_model.store_user_data(auth_data["uid"], auth_and_resident_data)

            if user:
                reset_link = auth.generate_password_reset_link(
                    auth_data["email"], app=firebase_app
                )
                send_mail(
                    subject="The oneBarangay app has created an account for you.",
                    message=(
                        f"click <a href='{reset_link}'>here</a> \
                        to reset the password of the newly created account."
                    ),
                    from_email=os.getenv("ADMIN_EMAIL"),
                    recipient_list=[auth_data["email"]],
                )
        else:
            # For Local Testing.
            auth_data["uid"] = str(user.uid if user.uid else uuid.uuid4())
            auth_data["provider"] = "oneBarangay"
            time_now = datetime.now(tz=pytz.timezone("Asia/Manila"))
            auth_data["creation_date"] = datetime.timestamp(time_now) * 1000
            auth_data["last_sign_in"] = None
            auth_data["email_verified"] = False

        self.json.add_row_to_auth_json(auth_data)
        AzureStorageBlob(
            sas_token=os.getenv("AZURE_STORAGE_CONTAINER_SAS_AUTH"),
            blob_name=os.getenv("AZURE_STORAGE_BLOB_AUTH_NAME"),
        ).upload_local_json_file("auth_data.json")

    def modify_user(self, uid: str, user_info: dict) -> None:
        """Modify a user in Firebase Auth.

        Args:
          uid: str: The user id of user to be modified.
          user_info: dict: The user information of user to be modified.

        Returns:
          None.
        """
        db = firestore.client(app=firebase_app)
        if os.getenv("GAE_ENV", "").startswith("standard"):
            # TODO: Add action for reset password
            # TODO: Listen for last_sign_in

            # Update User Collection
            db.collection("users").document(uid).update(user_info)

            user = auth.update_user(
                uid,
                email=user_info.get("email"),
                display_name=user_info.get("display_name"),
                disabled=user_info.get("disabled"),
                photo_url=user_info.get("photo_url"),
                phone_number=user_info.get("phone_number"),
                app=firebase_app,
            )
            auth.set_custom_user_claims(user.uid, {user_info["role"]: True}, app=firebase_app)
        else:
            # For Local Testing.
            user_info["uid"] = uid
            user_info["provider"] = "oneBarangay"
            user_info["creation_date"] = datetime.now(tz=pytz.timezone("Asia/Manila")).timestamp()
            user_info["last_sign_in"] = None
            user_info["email_verified"] = False

        updated_user = db.collection("users").document(uid).get().to_dict()
        updated_user.pop("updated_on")
        self.json.modify_row_in_auth_json(updated_user)

        AzureStorageBlob(
            sas_token=os.getenv("AZURE_STORAGE_CONTAINER_SAS_AUTH"),
            blob_name=os.getenv("AZURE_STORAGE_BLOB_AUTH_NAME"),
        ).upload_local_json_file("auth_data.json")

    def delete_user(self, uid: str):
        """Delete a user from Firebase Auth.

        Args:
          uid: str: The user id of the user to be deleted.

        Returns:
          None.
        """
        try:
            if os.getenv("GAE_ENV", "").startswith("standard"):
                auth.delete_user(uid, app=firebase_app)
                return True
        except UserNotFoundError:
            logger.exception(
                "[FirebaseAuth.delete_user] User %s not found in Firebase Auth.", uid
            )
            return False

        self.json.delete_row_in_auth_json(uid)
        AzureStorageBlob(
            sas_token=os.getenv("AZURE_STORAGE_CONTAINER_SAS_AUTH"),
            blob_name=os.getenv("AZURE_STORAGE_BLOB_AUTH_NAME"),
        ).upload_local_json_file("auth_data.json")

"""Module for sending notifications."""
from datetime import datetime

import pytz
from django.templatetags.static import static
from firebase_admin import messaging

from one_barangay.settings import firebase_app, firestore_db


class Notification:
    """Class for notification."""

    def get_registration_token(self, platform: str, user_id=None):
        """Get registration tokens.

        Args:
          platform: str: The type of platform the notification is.
          user_id: str: The unique id of the user to send notification.

        Returns:
          None.
        """
        if user_id:
            user_data = firestore_db.collection("users").document(user_id).get().to_dict()
            if platform != "all":
                registration_id = user_data.get(f"{platform}_notification")
            else:
                registration_id = [
                    user_data.get("web_notification"),
                    user_data.get("mobile_notification"),
                ]
        else:
            user_docs = firestore_db.collection("users").stream()

            registration_id = []
            for doc in user_docs:
                user_data = firestore_db.collection("users").document(doc.id).get().to_dict()

                if platform != "all":
                    registration_id.append(user_data.get(f"{platform}_notification"))
                else:
                    registration_id.append(user_data.get("web_notification"))
                    registration_id.append(user_data.get("mobile_notification"))

        registration_list = list(filter(None, registration_id))
        return registration_list[0] if len(registration_list) == 1 else registration_list

    def send_notification(
        self, title: str, body: str, user_id: str = None, platform: str = "all"
    ):
        """Send notification.

        Args:
          title: str: The title of the notification.
          body: str: The message of the notification.
          user_id: str: The unique id of the user to be notified.
          platform: str: The type of platform the notification is.

        Returns:
          None.
        """
        registration_token = self.get_registration_token(platform, user_id)
        message_data = {
            "title": title,
            "body": body,
            "icon": static("/assets/img/favicon/favicon.ico"),
            "requireInteraction": "true",
        }

        if isinstance(registration_token, list):

            message = messaging.MulticastMessage(
                data=message_data,
                tokens=registration_token,
            )
            messaging.send_multicast(message, app=firebase_app)
        else:
            message = messaging.Message(
                data=message_data,
                token=registration_token,
            )
            messaging.send(message, app=firebase_app)

        self.save_notification(registration_token, message_data, platform)

    def save_notification(self, registration_token, notification_data, platform):
        """Save notification.

        Args:
          registration_token: str: The token for notification.
          notification_data: str: The data to be saved.
          platform: str: The type of platform the notification is.

        Returns:
          None.
        """
        device = "web" if platform == "all" else platform

        if isinstance(registration_token, list):
            for token in registration_token:
                notification_query = (
                    firestore_db.collection("users")
                    .where(f"{device}_notification", "==", token)
                    .get()[0]
                )

                if notification_query.exists:
                    user_id = notification_query.id
                    (
                        firestore_db.collection("users")
                        .document(user_id)
                        .collection("notification")
                        .add(
                            notification_data
                            | {"time": datetime.now(tz=pytz.timezone("Asia/Manila"))}
                        )
                    )
        else:
            notification_query = (
                firestore_db.collection("users")
                .where(f"{device}_notification", "==", registration_token)
                .get()[0]
            )

            if notification_query.exists:
                user_id = notification_query.id
                (
                    firestore_db.collection("users")
                    .document(user_id)
                    .collection("notification")
                    .add(
                        notification_data
                        | {"time": datetime.now(tz=pytz.timezone("Asia/Manila"))}
                    )
                )

    def delete_notification(self, registration_token, notification_id, platform: str):
        """Delete notification.

        Args:
          registration_token: str: The token for notification.
          notification_id: The id of notification to delete.
          platform: str: The type of platform the notification is.

        Returns:
          None.
        """
        device = "web" if platform == "all" else platform

        if isinstance(registration_token, list):
            for token in registration_token:
                notification_query = (
                    firestore_db.collection("users")
                    .where(f"{device}_notification", "==", token)
                    .get()[0]
                )

                if notification_query.exists:
                    user_id = notification_query.id
                    if isinstance(notification_id, list):
                        for unique_id in notification_id:
                            (
                                firestore_db.collection("users")
                                .document(user_id)
                                .collection("notification")
                                .document(unique_id)
                                .delete()
                            )
                    else:
                        (
                            firestore_db.collection("users")
                            .document(user_id)
                            .collection("notification")
                            .document(notification_id)
                            .delete()
                        )
        else:
            notification_query = (
                firestore_db.collection("users")
                .where(f"{device}_notification", "==", registration_token)
                .get()[0]
            )

            if notification_query.exists:
                user_id = notification_query.id
                (
                    firestore_db.collection("users")
                    .document(user_id)
                    .collection("notification")
                    .document(notification_id)
                    .delete()
                )

"""Custom context processors."""
from one_barangay.settings import firestore_db


def get_notification(request):
    """Get notification of a logged in user.

    Args:
      request: The URL request.

    Returns:
      A list the users notification.
    """
    notification_data = (
        firestore_db.collection("users")
        .document(request.session["user"]["user_id"])
        .collection("notification")
        .order_by("time", direction="DESCENDING")
        .stream()
    )
    return {
        "notification_list": [notification.to_dict() for notification in list(notification_data)]
    }

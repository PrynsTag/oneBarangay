"""Hello World."""
import datetime

from django.shortcuts import render

# Database
from firebase_admin import firestore

from one_barangay.local_settings import firebase_app

# Create your views here.

db = firestore.client(firebase_app)


def index(request):
    """Render Service HTML.

    Args:
      request:

    Returns:
      : Display Service Page
    """
    # For Document Request
    user_sess_data = request.session["user"]

    document_ref = db.collection("document_request")

    request_status = None
    if user_sess_data["role"] in ["admin", "head_admin", "secretary", "worker"]:
        request_status = document_ref.where("status", "==", "request").get()
    else:
        request_status = (
            document_ref.where("status", "==", "request")
            .where("user_id", "==", user_sess_data["user_id"])
            .get()
        )

    request_list = [request.to_dict() for request in request_status]

    # For Appointment Query
    appointment_ref = db.collection("appointments")
    appointments = None

    if user_sess_data["role"] in ["admin", "head_admin", "secretary", "worker"]:
        appointments = appointment_ref.stream()
    else:
        appointments = appointment_ref.where("user_id", "==", user_sess_data["user_id"]).stream()

    appointments_data = [data.to_dict() for data in appointments]

    return render(
        request,
        "services/service.html",
        {
            "request_count": len(request_list),
            "appointment_count": len(appointments_data),
            "date": datetime.date.today(),
            "user_sess_data": user_sess_data,
        },
    )

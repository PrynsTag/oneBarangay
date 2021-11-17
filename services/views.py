"""Hello World."""
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
    request_status = db.collection("document_request").where("status", "==", "request").get()
    request_list = [request.to_dict() for request in request_status]

    # For Appointment Query

    # For Complaints

    # For Bulk Schedule

    return render(request, "services/service.html", {"request_count": len(request_list)})

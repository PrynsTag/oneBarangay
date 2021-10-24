"""Create your complaint url routing here."""
from django.urls import path

from . import views

app_name = "complaint"

urlpatterns = [
    path(
        "home",
        views.ComplaintHomeView.as_view(
            extra_context={"title": "Complaint", "segment": "complaint"}
        ),
        name="home",
    ),
    path(
        "create",
        views.ComplaintCreateView.as_view(
            extra_context={"title": "Create complaint", "segment": "complaint"}
        ),
        name="create",
    ),
    path(
        "detail/<str:complaint_id>",
        views.ComplaintDetailView.as_view(
            extra_context={"title": "Complaint Detail", "segment": "complaint"}
        ),
        name="detail",
    ),
]

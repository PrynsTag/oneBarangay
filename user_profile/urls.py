"""Create your url routing for user_profile here."""
from django.urls import path

from . import views

app_name = "user_profile"

urlpatterns = [
    path(
        "",
        views.UserProfileFormView.as_view(
            extra_context={"title": "User Profile"},
        ),
        name="user_profile",
    )
]

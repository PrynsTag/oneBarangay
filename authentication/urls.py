"""Create your URL Routing for authentication here."""
from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    path(
        "login",
        views.AuthenticationFormView.as_view(extra_context={"title": "Sign In"}),
        name="sign_in",
    ),
    path(
        "register",
        views.AuthenticationFormView.as_view(
            extra_context={"title": "Sign Up"},
        ),
        name="sign_up",
    ),
    path(
        "forgot-password",
        views.ForgotPasswordFormView.as_view(
            extra_context={"title": "Forgot Password"},
        ),
        name="forgot_password",
    ),
    path(
        "lock-account",
        views.LockAccountFormView.as_view(
            extra_context={"title": "Lock Account"},
        ),
        name="lock_account",
    ),
    path(
        "firebase_login",
        views.login,
        name="firebase_login",
    ),
    path("logout", views.logout, name="logout"),
]

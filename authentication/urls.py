"""Create your URL Routing for authentication here."""
from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    path(
        "login", views.LoginFormView.as_view(extra_context={"title": "Sign In"}), name="sign_in"
    ),
    path(
        "register",
        views.RegisterFormView.as_view(
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
]

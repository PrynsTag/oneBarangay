"""Create your URL Routing for authentication here."""
from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    path(
        "firebase_login",
        views.login,
        name="firebase_login",
    ),
    path(
        "firebase_register",
        views.register,
        name="firebase_register",
    ),
    path(
        "register",
        views.AuthenticationFormView.as_view(
            extra_context={"title": "Sign Up"},
        ),
        name="register",
    ),
    path(
        "login",
        views.AuthenticationFormView.as_view(
            extra_context={"title": "Sign In"},
        ),
        name="sign_in",
    ),
    path(
        "setup/<str:user_id>",
        views.AccountSetupFormView.as_view(
            extra_context={"title": "Account Setup"},
        ),
        name="setup",
    ),
    path("logout", views.logout, name="logout"),
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

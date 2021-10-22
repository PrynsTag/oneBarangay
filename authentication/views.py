"""Create your authentication views here."""
import json
import os
from typing import Union

from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.generic import FormView
from firebase_admin import auth
from firebase_admin.auth import UserRecord

from ocr.firestore_model import FirestoreModel
from one_barangay.local_settings import logger
from one_barangay.scripts.storage_backends import AzureStorageBlob
from one_barangay.settings import firebase_app
from user_management.json_functions import UserManagementJSON
from user_profile.models import UserModel

from .forms import AuthenticationForm, ForgotPasswordForm, LockAccountForm
from .models import AuthModel


# TODO: Fix client-side validation
class AuthenticationFormView(FormView):
    """Form view for login."""

    template_name = "authentication/authentication.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("data_viz:dashboard")
    error_css_class = "invalid-feedback"
    required_css_class = "required"

    def form_valid(self, form) -> HttpResponse:
        """Authenticate user when login form is valid.

        Args:
          form: The html login form submitted.

        Returns:
          HttpResponse: Redirects to dashboard.
        """
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        authenticate(username=username, password=password)

        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponse:
        """Return login form with errors when login form is invalid.

        Args:
          form: The html login form submitted.

        Returns:
          Render form with errors.
        """
        messages.error(self.request, "Invalid credentials.")

        return super().form_invalid(form)


class ForgotPasswordFormView(FormView):
    """Form view for forgot password form."""

    template_name = "authentication/authentication.html"
    form_class = ForgotPasswordForm
    success_url = reverse_lazy("auth:sign_in")

    def form_valid(self, form) -> HttpResponse:
        """Send a password reset email to a user when login form is valid.

        Args:
          form: The html forgot password form submitted.

        Returns:
          None: Redirects to login.
        """
        reset_link = auth.generate_password_reset_link(
            form.cleaned_data["email"], app=firebase_app
        )
        send_mail(
            subject="Password reset",
            message=f"click <a href='{reset_link}'>here</a> to reset your password.",
            from_email=os.getenv("ADMIN_EMAIL"),
            recipient_list=[form.cleaned_data["email"]],
        )
        messages.success(
            self.request, "Password reset link sent! Check your email for the reset link."
        )

        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponse:
        """Return forgot password form with errors when login form is invalid.

        Args:
          form: The html forgot password form submitted

        Returns:
          Render form with errors.
        """
        messages.error(self.request, "Password reset not sent!")
        for field in form.errors:
            form[field].field.widget.attrs["class"] += " is-invalid"

        return super().form_invalid(form)


class LockAccountFormView(FormView):
    """Form view for lock account form."""

    template_name = "authentication/lock_account.html"
    form_class = LockAccountForm
    success_url = reverse_lazy("data_viz:dashboard")

    def form_valid(self, form) -> HttpResponse:
        """Authenticate locked user.

        Args:
          form: The LockAccountForm form submitted

        Returns:
          None: Redirects to dashboard.
        """
        messages.add_message(self.request, messages.SUCCESS, "Login successful!")

        return super().form_valid(form)

    def form_invalid(self, form):
        """Return LockAccountForm form with errors.

        Args:
          form: The LockAccountForm form submitted

        Returns:
          Render LockAccountForm form with errors.
        """
        messages.add_message(
            self.request, messages.ERROR, f"Login not successful!\n{form.errors}"
        )

        return super().form_invalid(form)


def login(request):
    """Log user in.

    Associate barangay data with authentication data and store in session.
    Args:
      request: The URL Request.

    Returns:
      Render form with errors.
    """
    data = json.load(request)
    auth_data: dict = data.get("payload")

    if auth_data["newUser"]:
        # Set user role.
        auth.set_custom_user_claims(auth_data["uid"], {"resident": True}, app=firebase_app)

        # Add new user to auth_data.json
        user: UserRecord = auth.get_user(auth_data["uid"], firebase_app)
        firebase_auth_data = {
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
        resident_data = FirestoreModel().get_resident_rbi(auth_data)

        auth_and_resident_data = auth_data | resident_data | firebase_auth_data

        # Add new user to firestore rbi collection.
        auth_model = AuthModel()
        connect_auth_to_rbi = auth_model.connect_data_to_rbi(auth_and_resident_data)

        # Store user to firestore users collection.
        auth_model.store_user_data(auth_data["uid"], auth_and_resident_data)

        # Store firebase auth data to user_management json.
        UserManagementJSON().add_row_to_auth_json(firebase_auth_data)
        AzureStorageBlob(
            sas_token=os.getenv("AZURE_STORAGE_CONTAINER_SAS_AUTH"),
            blob_name=os.getenv("AZURE_STORAGE_BLOB_AUTH_NAME"),
        ).upload_local_json_file("auth_data.json")

        request.session["user"] = auth_and_resident_data
        # TODO: Display Modal to input credentials 'Let us setup your account'".
        if connect_auth_to_rbi:
            logger.info("User connected to rbi data.")
        else:
            logger.info("User not connected to rbi data.")
    else:
        request.session["user"] = UserModel().get_user_data(auth_data["uid"])
        # Replace firstname with email and lastname with blank
        first_name = request.session["user"].get("first_name")
        photo_url = request.session["user"].get("photo_url")

        if not first_name:
            request.session["user"]["first_name"] = request.session["user"]["email"].split("@")[0]
            request.session["user"]["last_name"] = ""

        if not photo_url:
            request.session["user"]["photo_url"] = static("/assets/img/icons/default_user.svg")

    return HttpResponse("OK")


def logout(request) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
    """Log user out.

    Delete user session.
    Args:
      request: The URL Request.

    Returns:
      Redirect to home.
    """
    try:
        del request.session["user"]

        messages.success(request, "Logged out successfully.")
        logger.info("[logout] successfully logout.")
    except KeyError:
        logger.exception("No logged in user.")

    return redirect("auth:sign_in")

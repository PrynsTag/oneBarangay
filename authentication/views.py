"""Create your authentication views here."""
import json
import os
from typing import Union

from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.generic import FormView
from firebase_admin import auth
from firebase_admin.auth import UserRecord

from one_barangay import settings
from one_barangay.local_settings import logger
from one_barangay.mixins import FormInvalidMixin
from one_barangay.settings import firebase_app, firestore_db

from .forms import AccountSetupForm, AuthenticationForm, ForgotPasswordForm, LockAccountForm


# TODO: Fix client-side validation
class AuthenticationFormView(FormInvalidMixin, FormView):
    """Form view for login."""

    template_name = "authentication/authentication.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("data_viz:dashboard")
    error_message = "Invalid credentials."

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


class AccountSetupFormView(FormInvalidMixin, FormView):
    """Form view for account setup."""

    template_name = "authentication/account_setup.html"
    form_class = AccountSetupForm
    success_url = reverse_lazy("user_profile:home")
    error_message = "Invalid credentials."

    # def get(self, request, *args, **kwargs) -> HttpResponse:
    #     """GET request to display rbi collection to ocr home.
    #
    #     Args:
    #       request: The URL request.
    #       **args: Additional arguments.
    #       **kwargs: Additional keyword arguments.
    #
    #     Returns:
    #       The firestore rbi collection data.
    #     """
    #     context = self.get_context_data(**kwargs)
    #     context["user_id"] = kwargs["user_id"]
    #
    #     return self.render_to_response(context)

    def form_valid(self, form) -> HttpResponse:
        """Authenticate user when login form is valid.

        Args:
          form: The html login form submitted.

        Returns:
          HttpResponse: Redirects to dashboard.
        """
        user_id = self.kwargs["user_id"]

        first_name = form.cleaned_data["first_name"]
        middle_name = form.cleaned_data.get("middle_name")
        last_name = form.cleaned_data["last_name"]

        street = form.cleaned_data["street"]
        contact_number = form.cleaned_data.get("contact_number")
        birth_place = form.cleaned_data["birth_place"]
        date_of_birth = form.cleaned_data["date_of_birth"].strftime("%B %d, %Y")

        user_col = firestore_db.collection("users")
        rbi_col = firestore_db.collection("rbi")

        last_name_query = rbi_col.where("family_name", "==", last_name)
        street_compound_query = last_name_query.where("street", "==", street).get()[0]

        # TODO: Add address to query.
        if street_compound_query.exists:
            rbi_doc = rbi_col.document(street_compound_query.id)
            rbi_data = rbi_doc.get().to_dict()

            rbi_data.pop("creation_date")
            rbi_data.pop("date_accomplished")

            if rbi_data:
                family_sub_col = rbi_doc.collection("family")

                date_of_birth_query = family_sub_col.where("date_of_birth", "==", date_of_birth)
                birth_place_compound_query = date_of_birth_query.where(
                    "birth_place", "==", birth_place
                )
                last_name_compound_query = birth_place_compound_query.where(
                    "last_name", "==", last_name
                ).get()[0]

                first_name_query = family_sub_col.where("first_name", "==", first_name).get()[0]
                if contact_number:
                    contact_number_query = (
                        family_sub_col.where("contact_number", "==", contact_number).get().exists
                    )
                else:
                    contact_number_query = False
                if middle_name:
                    middle_name_query = (
                        family_sub_col.where("middle_name", "==", middle_name).get()[0].exists
                    )
                else:
                    middle_name_query = False

                query = [
                    last_name_compound_query.exists,
                    first_name_query.exists,
                    contact_number_query,
                    middle_name_query,
                ]

                # Check if query has more than one correct result.
                if query.count(True) >= 1:
                    member_id = last_name_compound_query.id
                    family_member_doc = family_sub_col.document(member_id)
                    member_data = family_member_doc.get().to_dict()

                    user_ref = user_col.document(user_id)
                    user = auth.get_user(user_id, firebase_app)
                    account_data = {
                        "provider": user.provider_id,
                        "creation_date": user.user_metadata.creation_timestamp,
                        "last_sign_in": user.user_metadata.last_sign_in_timestamp,
                    }
                    user_info = {
                        "user_id": user_id,
                        "display_name": user.display_name,
                        "email": user.email,
                        "role": "resident",
                        "email_verified": user.email_verified,
                        "disabled": user.disabled,
                        "new_user": False,
                    }

                    user_profile_data = rbi_data | member_data | user_info
                    # Save user profile data to users collection.
                    user_ref.set(user_profile_data, merge=True)
                    # Set user session data.
                    self.request.session["user"] = user_profile_data

                    user_ref.collection("account").document(user_id).set(account_data)

                    # Save family info in family sub-collection.
                    family_doc = rbi_doc.collection("family").stream()
                    for member in family_doc:
                        user_ref.collection("family").document(user_id).set(member.to_dict())

                    family_member_data = form.cleaned_data | member_data | user_info
                    family_member_doc.set(family_member_data, merge=True)

                    messages.info(
                        self.request,
                        "User has been successfully verified and is a resident of barangay!",
                    )
        else:
            self.request.session["user"]["not_resident"] = True
            messages.info(
                self.request,
                "User not found in the barangay's record! Limited functionality are observed.",
            )

        return super().form_valid(form)
        # return JsonResponse({"success": "Successfully setup account!"}, status=200)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to account_setup form view.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          The dictionary data needed by account_setup form view.
        """
        context = super().get_context_data()
        context["title"] = "Account Setup"
        context["first_row"] = ["first_name", "middle_name", "last_name"]
        context["second_row"] = ["date_of_birth", "birth_place"]

        context["first_address"] = ["city", "province", "street"]
        context["second_address"] = ["barangay", "region", "zip_code"]

        context["hidden_fields"] = ["country", "latitude", "longitude"]

        context["row_fields"] = context["first_row"] + context["second_row"]

        context["google_api_key"] = settings.GOOGLE_API_KEY

        return context


class ForgotPasswordFormView(FormInvalidMixin, FormView):
    """Form view for forgot password form."""

    template_name = "authentication/authentication.html"
    form_class = ForgotPasswordForm
    success_url = reverse_lazy("auth:sign_in")
    error_message = "Password reset not sent!"

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
        # TODO: Add html template.
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


class LockAccountFormView(FormInvalidMixin, FormView):
    """Form view for lock account form."""

    template_name = "authentication/lock_account.html"
    form_class = LockAccountForm
    success_url = reverse_lazy("data_viz:dashboard")
    error_message = "Login not successful! Please fix the error presented in the form."

    def form_valid(self, form) -> HttpResponse:
        """Authenticate locked user.

        Args:
          form: The LockAccountForm form submitted

        Returns:
          None: Redirects to dashboard.
        """
        messages.add_message(self.request, messages.SUCCESS, "Login successful!")

        return super().form_valid(form)


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

    user_col = firestore_db.collection("users")
    user_data = user_col.where("email", "==", auth_data["email"]).get()[0].to_dict()

    rbi_col = firestore_db.collection("rbi")

    # Query the user in rbi if it exits in RBI.
    family_name_query = rbi_col.where("family_name", "==", user_data["last_name"])
    street_query = family_name_query.where("street", "==", user_data["street"]).get()[0]

    # Query in family sub-col if it exists
    family_col = rbi_col.document(street_query.id).collection("family")
    last_name_query = family_col.where("last_name", "==", user_data["last_name"])
    date_of_birth_query = last_name_query.where(
        "date_of_birth", "==", user_data["date_of_birth"]
    ).get()[0]

    if date_of_birth_query.exists:
        resident_data = family_col.document(date_of_birth_query.id).get().to_dict()
    else:
        resident_data = {}

    request.session["user"] = resident_data | user_data

    # Replace firstname with email and lastname with blank
    first_name = request.session["user"].get("first_name")
    photo_url = request.session["user"].get("photo_url")
    email = auth_data.get("email")
    # if not request.session["user"] and auth_data.get("email"):
    if not first_name and email:
        request.session["user"]["email"] = email
        request.session["user"]["first_name"] = email.split("@")[0]
        request.session["user"]["last_name"] = ""

    if not photo_url:
        request.session["user"]["photo_url"] = static("/assets/img/icons/default_user.svg")

    return JsonResponse({"message": "Successfully logged in!"}, status=200)


def register(request):
    """Register user.

    Args:
      request: The URL Request.

    Returns:
      Render form with errors.
    """
    data = json.load(request)
    auth_data: dict = data.get("payload")
    user_id = auth_data["user_id"]

    # Set user role.
    auth.set_custom_user_claims(user_id, {"resident": True}, app=firebase_app)
    user: UserRecord = auth.get_user(user_id, firebase_app)
    account_data = {
        "provider": user.provider_id,
        "creation_date": user.user_metadata.creation_timestamp,
        "last_sign_in": user.user_metadata.last_sign_in_timestamp,
    }
    user_data = {
        "user_id": user.uid,
        "display_name": user.display_name,
        "email": user.email,
        "role": "resident",
        "email_verified": user.email_verified,
        "disabled": user.disabled,
        "contact_number": user.phone_number,
        "photo_url": user.photo_url,
        "new_user": auth_data["newUser"],
    }

    user_col = firestore_db.collection("users")

    user_col.document(user_id).set(user_data)
    user_col.document(user_id).collection("account").add(account_data)

    # TODO: Display Modal to input credentials 'Let us setup your account'".
    # TODO: family col first_name, last_name, date_of_birth.
    # TODO: RBI col address, family_name.
    return JsonResponse({"message": "Successfully registered!"}, status=200)


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

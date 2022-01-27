"""Create your views here."""
import os
from datetime import date, datetime
from typing import Union

from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.generic import FormView
from firebase_admin import auth, firestore
from firebase_admin.auth import EmailAlreadyExistsError, UidAlreadyExistsError, UserNotFoundError
from google.api_core.exceptions import NotFound

from one_barangay.local_settings import logger
from one_barangay.mixins import FormInvalidMixin
from one_barangay.notification import Notification
from one_barangay.settings import firebase_app

# TODO: send email delete account.
from user_management.forms import UserManagementCreateForm


class UserManagementHomeView(FormInvalidMixin, FormView):
    """Form for adding user."""

    template_name = "user_management/home.html"
    form_class = UserManagementCreateForm
    success_url = reverse_lazy("user_management:home")
    error_message = "User creation not successful! Please fix the errors displayed in the form!"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Get single complaint from firestore.

        Args:
          request: The URL request.
          *args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          Render HttpResponse to complaint/home.html along with context data.
        """
        context = self.get_context_data(**kwargs)

        db = firestore.client(app=firebase_app)
        docs = db.collection("users").where("user_id", ">", "").stream()

        users = []
        for doc in docs:
            user = doc.to_dict()
            # Calculate Age
            if user.get("birth_date"):
                today = date.today()
                birth_date_dt = datetime.strptime(user["birth_date"], "%B %d, %Y")
                age = (
                    today.year
                    - birth_date_dt.year
                    - ((today.month, today.day) < (birth_date_dt.month, birth_date_dt.day))
                )
                user["age"] = age
            # Convert Unix Timestamp to Human Date.
            if user.get("creation_date"):
                try:
                    user["creation_date"] = datetime.fromtimestamp(user["creation_date"] / 1000).strftime(
                        "%A, %B %d %Y, %H:%M %p"
                    )
                except ValueError:
                    user["creation_date"] = None

            if user.get("last_sign_in"):
                user["last_sign_in"] = datetime.fromtimestamp(user["last_sign_in"] / 1000)

            users.append(user)

        context["users"] = users

        return self.render_to_response(context)

    def form_valid(self, form, **kwargs) -> HttpResponse:
        """Call when UserManagementCreateForm is valid.

        Args:
          form: The submitted UserManagementCreateForm form.
          **kwargs: Keyword arguments.

        Returns:
          Redirect to user_management home.
        """
        logger.info("Creating user..")

        image = form.cleaned_data["photo_url"]
        if image:
            filename = default_storage.generate_filename(image.name)
            default_storage.save(filename, image)
            form.cleaned_data["photo_url"] = default_storage.url(filename)
            form.cleaned_data["image"] = filename

        # # Get only truthy form fields
        truthy_values = {k: v for k, v in form.cleaned_data.items() if v}
        truthy_values["disabled"] = truthy_values["disabled"] == "True"

        # Format / clean auth data
        user_auth_data = truthy_values.copy()
        role = user_auth_data.pop("role")
        if user_auth_data.get("image"):
            del user_auth_data["image"]

        try:
            user = auth.create_user(**user_auth_data, app=firebase_app)
            auth.set_custom_user_claims(user.uid, {role: True}, app=firebase_app)

            if user.display_name:
                first_name, last_name = user.display_name.split()
            else:
                first_name, last_name = None, None

            auth_data = {
                "user_id": user.uid,
                "display_name": user.display_name,
                "first_name": first_name,
                "last_name": last_name,
                "email": user.email,
                "role": role,
                "provider": user.provider_id,
                "creation_date": user.user_metadata.creation_timestamp,
                "last_sign_in": user.user_metadata.last_sign_in_timestamp,
                "email_verified": user.email_verified,
                "disabled": user.disabled,
                "phone_number": user.phone_number,
                "photo_url": user.photo_url,
            }

            # Store Firebase Auth data to Firestore Users Collection
            db = firestore.client(app=firebase_app)
            db.collection("users").document(user.uid).set(auth_data, merge=True)

            # Generate password reset link.
            reset_link = auth.generate_password_reset_link(
                form.cleaned_data["email"],
                app=firebase_app,
            )
            # TODO: Add html template.
            send_mail(
                subject="The oneBarangay app has created an account for you.",
                message="You received this because your barangay has created you an account.",
                html_message=f"click <a href='{reset_link}'>here</a> to setup your password",
                from_email=os.getenv("ADMIN_EMAIL"),
                recipient_list=[form.cleaned_data["email"]],
            )

            logger.info("Successfully created new user with role: %s", form.cleaned_data["role"])
            messages.success(
                self.request,
                (
                    f"Created new user with role: {form.cleaned_data['role']}. "
                    "A password reset link has also been sent."
                ),
            )
        except EmailAlreadyExistsError:
            logger.exception("User with email %s already exists!", form.cleaned_data["email"])
            messages.error(
                self.request,
                f"User with email {form.cleaned_data['email']} already exists!",
            )
        except UidAlreadyExistsError:
            logger.exception("User with uid %s already exists!", form.cleaned_data["user_id"])
            messages.error(
                self.request,
                f"User with uid {form.cleaned_data['user_id']} already exists!",
            )

        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to user_management.

        Get the json url file, segment, form and title to display user table.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          The dictionary data needed by user_management index.
        """
        context = super().get_context_data()

        context["segment"] = "user_management"
        context["title"] = "User Management"
        context["sub_title"] = "Manage user accounts in oneBarangay."
        context["id"] = "uid"
        context["default_image"] = static("/assets/img/icons/default_user.svg")
        context["sort"] = [
            {"sortName": "creation_date", "sortOrder": "desc"},
            {"sortName": "display_name", "sortOrder": "asc"},
            {"sortName": "disabled", "sortOrder": "desc"},
        ]

        return context


# TODO: disabled accounts must not be logged in.
class UserManagementEditView(UserManagementHomeView, FormInvalidMixin):
    """Form for editing a user."""

    error_message = "Modifying not successful! Please fix the errors displayed in the form!"

    def form_valid(self, form, **kwargs) -> HttpResponse:
        """Call when UserManagementCreateForm is valid.

        Args:
          form: The UserManagementCreateForm submitted.
          **kwargs: Keyword arguments.

        Returns:
          Redirect to user_management index.
        """
        logger.info("Modifying user: %s", form.cleaned_data["user_id"])

        # Get only truthy form fields
        changed_fields = {k: v for k, v in form.cleaned_data.items() if v}
        changed_fields["disabled"] = changed_fields["disabled"] == "True"
        # Format / clean data for auth.update_user
        auth_data = changed_fields.copy()
        if changed_fields.get("role"):
            auth_data["custom_claims"] = {changed_fields["role"]: True}
            del auth_data["role"]
        if changed_fields.get("user_id"):
            del auth_data["user_id"]

        try:
            # Remove contact_number key from auth_data.
            auth_data["phone_number"] = auth_data["contact_number"]
            auth_data.pop("contact_number")

            # Modify Firebase Auth
            auth.update_user(form.cleaned_data["user_id"], **auth_data, app=firebase_app)

            # Modify Firestore User Collection
            db = firestore.client(app=firebase_app)
            changed_fields["updated_on"] = firestore.SERVER_TIMESTAMP
            db.collection("users").document(form.cleaned_data["user_id"]).update(changed_fields)

            logger.info(
                "Successfully updated user: %s",
                form.cleaned_data["email"],
            )
            messages.success(
                self.request,
                f"Successfully updated user: {form.cleaned_data['email']}",
            )
            user_id = form.cleaned_data["user_id"]
            email = form.cleaned_data["email"]

            notification = Notification()
            notification.send_notification(
                "Account Notification.",
                "Your account has been modified by an admin.",
                user_id,
            )
            send_mail(
                subject="Account Notification.",
                message="Your account has been modified by an admin.",
                from_email=os.getenv("ADMIN_EMAIL"),
                recipient_list=[email],
            )
        except NotFound:
            logger.exception("User %s doesn't exists!", form.cleaned_data["email"])
            messages.error(self.request, "User %s doesn't exists!", form.cleaned_data["email"])

        return HttpResponseRedirect(self.get_success_url())


def delete(request, user_id) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
    """Delete user account.

    Args:
      request: The URL request.
      user_id: The unique I.D. of the user to delete.

    Returns:
      Redirect to user_management home.
    """
    db = firestore.client(app=firebase_app)
    try:
        notification = Notification()
        notification.send_notification(
            "Account Notification.",
            "Your account has been modified by an admin.",
            user_id,
        )
        # Delete from Firebase Auth
        auth.delete_user(user_id, app=firebase_app)

        user_ref = db.collection("users").document(user_id)
        user_data = user_ref.get().to_dict()
        send_mail(
            subject="Account Notification.",
            message="Your account has been modified by an admin.",
            from_email=os.getenv("ADMIN_EMAIL"),
            recipient_list=[user_data["email"]],
        )

        # Delete from Firestore
        user_ref.delete()

        logger.info("Successfully deleted user: %s", user_id)
        # TODO: Display Flash message in template.
        messages.success(request, f"Successfully deleted user: %{user_id}")
    except UserNotFoundError:
        logger.exception("User %s Not Found!", user_id)
        messages.error(request, f"User ${user_id} Not Found!")

    return redirect("user_management:home")


def reset(request, email) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
    """Reset user password.

    Args:
      request: The URL request.
      email: The email to send the reset password.

    Returns:
      Redirect to user_management home.
    """
    try:
        reset_link = auth.generate_password_reset_link(email, app=firebase_app)
        # TODO: Add html template.
        # https://stackoverflow.com/a/28476681/11668142
        send_mail(
            subject="Password reset",
            message="You are receiving this because you requested a password reset.",
            html_message=f"<a href='{reset_link}'>click here</a> to reset your password",
            from_email=os.getenv("ADMIN_EMAIL"),
            recipient_list=[email],
        )
        messages.success(request, "Password reset link sent! Check your email for the reset link.")
    except KeyError:
        messages.error(request, "Password reset failed!.")
        logger.exception("Password reset failed!")

    return redirect("user_management:home")

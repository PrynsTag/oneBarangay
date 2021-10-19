"""Create your views here."""
import json
import os
from typing import Union

from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from one_barangay.local_settings import logger
from one_barangay.scripts.storage_backends import AzureStorageBlob
from user_management.forms import AddUserForm
from user_management.models import FirebaseAuth


# TODO: Send email signup invitation.
# TODO: send email delete account.
class AddUserFormView(FormView):
    """Form for adding user."""

    template_name = "user_management/user_table.html"
    form_class = AddUserForm
    success_url = reverse_lazy("user_management:user_management")

    def form_valid(self, form, **kwargs) -> HttpResponse:
        """Call when AddUserForm is valid.

        Args:
          form: The submitted AddUserForm form.
          **kwargs: Keyword arguments.

        Returns:
          Redirect to user_management index.
        """
        auth = FirebaseAuth()

        logger.info("Creating user..")

        image = form.cleaned_data["photo_url"]

        if image:
            default_storage.save(image.name, image)
            form.cleaned_data["photo_url"] = default_storage.url(image.name)

        # Get only modified (truthy) form fields
        truthy_values = {k: v for k, v in form.cleaned_data.items() if v}
        truthy_values["disabled"] = truthy_values["disabled"] == "True"

        auth.add_user(truthy_values)

        logger.info("Successfully created new user with role: %s", form.cleaned_data["role"])
        messages.success(
            self.request,
            f"Successfully created new user with role: {form.cleaned_data['role']}",
        )

        return super().form_valid(form)

    def form_invalid(self, form, **kwargs) -> HttpResponse:
        """Return lock account form with errors.

        Args:
          form: The submitted AddUserForm form.
          **kwargs: Keyword arguments.

        Returns:
          Redirect to user_management index with form errors.
        """
        messages.error(self.request, f"User creation not successful!\n{form.errors}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to user_management.

        Get the json url file, segment, form and title to display user table.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          The dictionary data needed by user_management index.
        """
        if os.getenv("GAE_ENV", "").startswith("standard"):
            url = AzureStorageBlob(
                sas_token=os.getenv("AZURE_STORAGE_CONTAINER_SAS_AUTH"),
                blob_name=os.getenv("AZURE_STORAGE_BLOB_AUTH_NAME"),
            ).file_url
        else:
            # run ./simple_cors_server.py
            url = "http://127.0.0.1:9000/auth_data.json"

        return {
            "url": url,
            "segment": "user_management",
            "form": self.form_class,
            "title": "User Management",
        }


class EditUserFormView(AddUserFormView):
    """Form for editing a user."""

    def form_valid(self, form, **kwargs) -> HttpResponse:
        """Call when AddUserForm is valid.

        Args:
          form: The AddUserForm submitted.
          **kwargs: Keyword arguments.

        Returns:
          Redirect to user_management index.
        """
        auth = FirebaseAuth()

        logger.info("Modifying user: %s", form.cleaned_data["uid"])

        # Get only modified (truthy) form fields
        truthy_values = {k: v for k, v in form.cleaned_data.items() if v}
        truthy_values["disabled"] = truthy_values["disabled"] == "True"

        auth.modify_user(
            form.cleaned_data["uid"],
            truthy_values,
        )
        logger.info("Successfully updated user: %s", form.cleaned_data["email"])
        messages.success(self.request, f"Successfully updated user: {form.cleaned_data['email']}")

        return super().form_valid(form)

    def form_invalid(self, form, **kwargs) -> HttpResponse:
        """Call when AddUserForm is invalid.

        Args:
          form: The AddUserForm submitted.
          **kwargs: Keyword arguments.

        Returns:
          Redirect to user_management index with errors.
        """
        messages.error(self.request, f"Modifying not successful!\n{form.errors}")
        return super().form_invalid(form)


class DeleteUserFormView(AddUserFormView):
    """Form for deleting user."""

    def post(
        self, request, *args, **kwargs
    ) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
        """Call when submitted form action is POST.

        Delete a user from user_table.
        Args:
          request: The URL request.
          *args: Arguments.
          **kwargs: Keyword arguments.

        Returns:
          Redirect to user_management index.
        """
        data = json.load(request)
        form_data = data.get("payload")

        logger.info("Deleting user: %s", form_data["uid"])
        FirebaseAuth().delete_user(form_data["uid"])
        logger.info("Successfully deleted user: %s", form_data["uid"])
        messages.success(request, f"Successfully deleted user: {form_data['uid']}")

        return redirect("user_management:user_management")

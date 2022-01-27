"""Create your user_profile views here."""
import contextlib

from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from authentication.models import AuthModel
from one_barangay.local_settings import logger
from one_barangay.mixins import ContextPageMixin, FormInvalidMixin
from one_barangay.settings import firestore_db
from user_profile.forms import UserProfileForm


class UserProfileFormView(ContextPageMixin, FormInvalidMixin, FormView):
    """Form view for user_profile."""

    template_name = "user_profile/user_profile.html"
    segment = "user_profile"
    title = "User Profile"
    sub_title = "Manage your data on this page."
    form_class = UserProfileForm
    success_url = reverse_lazy("user_profile:home")
    error_message = "Form not updated! Please fix the error presented in the form."

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
        if request.session.get("user"):
            complaint = (
                firestore_db.collection("complaints").where("user_id", "==", request.session["user"]["user_id"]).get()
            )
            user_appointments = (
                firestore_db.collection("document_request")
                .where("user_id", "==", request.session["user"]["user_id"])
                .get()
            )
            user_data = (
                firestore_db.collection("users").where("user_id", "==", request.session["user"]["user_id"]).get()
            )

            context["complaints"] = [doc.to_dict() for doc in complaint]

            context["user_appointments"] = []
            for doc in user_appointments:
                appointment_data = doc.to_dict()
                document_data = appointment_data.pop("document")

                with contextlib.suppress(KeyError):
                    appointment_data["document"] = document_data[0]["document_name"]

                context["user_appointments"].append(appointment_data)

            context["user_data"] = [doc.to_dict() for doc in user_data]

        return self.render_to_response(context)

    def get_form_kwargs(self):
        """Pass request session to form."""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form, **kwargs) -> HttpResponse:
        """Call when UserProfileForm is valid.

        Args:
          form: The submitted UserProfileForm form.
          **kwargs: Keyword arguments.

        Returns:
          Redirect to auth logout.
        """
        # Format form fields to key and value pair.
        # TODO: Fix form.changed_data changing other input.
        # TODO: Add changing of photo and background.
        changed_fields = {}
        if form.has_changed():
            for field in form.changed_data:
                if field == "date_of_birth":
                    changed_fields[field] = form.cleaned_data["date_of_birth"].strftime("%B %d, %Y")
                else:
                    changed_fields[field] = form.cleaned_data[field]

        if changed_fields:
            self.request.session["user"].update(changed_fields)
            change_result = AuthModel().update_user_data(self.request.session["user"]["user_id"], changed_fields)
            if change_result:
                messages.success(self.request, "Profile updated successfully!\nYou are now logging out.")
                logger.info("[UserProfileFormView.form_valid] Form successfully updated.")
            else:
                messages.error(self.request, "Profile NOT updated!")
                logger.info("[UserProfileFormView.form_valid] Form NOT updated!")

        return super().form_valid(form)

"""Create your user_profile views here."""
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import FormView

from authentication.models import AuthModel
from one_barangay.local_settings import logger
from user_profile.forms import UserProfileForm


class UserProfileFormView(FormView):
    """Form view for user_profile."""

    template_name = "user_profile/user_profile.html"
    form_class = UserProfileForm
    error_css_class = "invalid-feedback"
    required_css_class = "required"

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
                if field == "birth_date":
                    changed_fields[field] = form.cleaned_data["birth_date"].strftime("%B %d, %Y")
                else:
                    changed_fields[field] = form.cleaned_data[field]

        if changed_fields:
            self.request.session["user"].update(changed_fields)
            change_result = AuthModel().update_user_data(
                self.request.session["user"]["uid"], changed_fields
            )
            if change_result:
                messages.success(
                    self.request, "Profile updated successfully!\nYou are now logging out."
                )
                logger.info("[UserProfileFormView.form_valid] Form successfully updated.")
            else:
                messages.error(self.request, "Profile NOT updated!")
                logger.info("[UserProfileFormView.form_valid] Form NOT updated!")

        return super().form_valid(form)

    def form_invalid(self, form, **kwargs) -> HttpResponse:
        """Call when UserProfileForm is invalid.

        Args:
          form: The submitted UserProfileForm form.
          **kwargs: Keyword arguments.

        Returns:
          Render UserProfileForm with errors.
        """
        messages.error(self.request, "Form not updated!")
        logger.error("Form not updated!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to user_profile.

        Get the segment, form and title to display view.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          The dictionary data needed by user_profile.
        """
        context = {
            "segment": "user_profile",
            "form": UserProfileForm(request=self.request),
            "title": "User Profile",
        }
        return context

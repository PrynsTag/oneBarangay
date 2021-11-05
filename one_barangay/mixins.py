"""Custom Mixins."""
from django.contrib import messages


class ContextPageMixin:
    """Custom Mixin for title and subtitle of a page."""

    def get_context_data(self, **kwargs):
        """Mixin to get initialize title and sub_title to a webpage.

        Args:
          **kwargs: Additional keyword arguments

        Returns:
          The super context with title and sub_title.
        """
        context = super().get_context_data(**kwargs)

        context["title"] = self.title
        context["sub_title"] = self.sub_title
        context["segment"] = self.segment

        return context


class FormInvalidMixin:
    """Custom mixin for form errors."""

    def form_invalid(self, form):
        """Call when AnnouncementCreateForm is INVALID.

        Args:
          form: The submitted AnnouncementEditForm.

        Returns:
          The invalid form submitted.
        """
        for field in form.errors:
            form[field].field.widget.attrs["class"] += " is-invalid"

        messages.error(
            self.request,
            self.error_message,
        )
        return super().form_invalid(form)

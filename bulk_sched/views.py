"""Create your bulk_sched views here."""
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from bulk_sched.forms import BulkSchedCreateForm


class BulkSchedCreateView(FormView):
    """Form view for creating bulk scheduling."""

    template_name = "bulk_sched/create.html"
    form_class = BulkSchedCreateForm
    success_url = reverse_lazy("bulk_sched:create")

    def form_valid(self, form):
        """Call when BulkSchedCreateForm is VALID.

        Args:
          form: The submitted BulkSchedCreateForm.

        Returns:
          The valid BulkSchedCreateForm submitted.
        """
        messages.success(self.request, "Post has been saved! Do you want to create another post?")

        return super().form_valid(form)

    def form_invalid(self, form):
        """Call when BulkSchedCreateForm is INVALID.

        Args:
          form: The submitted BulkSchedCreateForm.

        Returns:
          The invalid BulkSchedCreateForm submitted.
        """
        for field in form.errors:
            form[field].field.widget.attrs["class"] += " is-invalid"
        messages.error(self.request, "Post has not been saved!")

        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to announcement create view.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          The dictionary data needed by announcement create view.
        """
        context = super().get_context_data()
        context["segment"] = "bulk_sched"
        context["title"] = "Bulk Scheduling"
        context["sub_title"] = "Schedule mass events, appointments and notifications."

        return context

"""Create your bulk_sched views here."""
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from bulk_sched.forms import BarangayCertificate, BulkSchedCreateForm
from one_barangay.mixins import ContextPageMixin, FormInvalidMixin


class BulkSchedCreateView(FormInvalidMixin, ContextPageMixin, FormView):
    """Form view for creating bulk scheduling."""

    template_name = "bulk_sched/create.html"
    form_class = BulkSchedCreateForm
    success_url = reverse_lazy("bulk_sched:create")
    error_message = "Post has not been saved! Please fix the error presented in the form."
    title = "Bulk Scheduling"
    sub_title = "Schedule mass events, appointments and notifications."
    segment = "bulk_sched"

    def form_valid(self, form):
        """Call when BulkSchedCreateForm is VALID.

        Args:
          form: The submitted BulkSchedCreateForm.

        Returns:
          The valid BulkSchedCreateForm submitted.
        """
        messages.success(self.request, "Post has been saved! Do you want to create another post?")

        return super().form_valid(form)


class CedulaCreateView(FormInvalidMixin, ContextPageMixin, FormView):
    """Form view for creating cedula."""

    template_name = "cedula/create.html"
    form_class = BarangayCertificate
    success_url = reverse_lazy("cedula:create")
    error_message = "Post has not been saved! Please fix the error presented in the form."
    title = "Cedula"
    sub_title = "Create cedula for your residents in oneBarangay!"
    segment = "cedula"

    def form_valid(self, form):
        """Call when BarangayCertificate is VALID.

        Args:
          form: The submitted BulkSchedCreateForm.

        Returns:
          The valid BulkSchedCreateForm submitted.
        """
        messages.success(self.request, "Post has been saved! Do you want to create another post?")

        return super().form_valid(form)

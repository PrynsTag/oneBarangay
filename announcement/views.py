"""Create your announcement views here."""

from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from firebase_admin import firestore

from announcement.forms import AnnouncementCreateForm, AnnouncementEditForm
from one_barangay.settings import firebase_app


class AnnouncementHomeView(TemplateView):
    """Template view for announcement home."""

    template_name = "announcement/home.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Get all announcement from firestore.

        Args:
          request: The URL request.
          *args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          Render HttpResponse to announcement/home.html along with context data.
        """
        context = self.get_context_data(**kwargs)
        db = firestore.client(app=firebase_app)

        docs = db.collection("announcements").order_by("created", direction="DESCENDING").stream()
        announcements = [doc.to_dict() for doc in docs]
        context["announcements"] = announcements

        return self.render_to_response(context)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to announcement create view.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          The dictionary data needed by announcement create view.
        """
        context = super().get_context_data()
        context["segment"] = "announcement"
        context["title"] = "Announcement"
        context["sub_title"] = "View announcements / events created by oneBarangay."

        return context


class AnnouncementCreateView(FormView):
    """Form view for creating announcement."""

    form_class = AnnouncementCreateForm
    template_name = "announcement/create.html"
    success_url = reverse_lazy("announcement:create")

    def get_form_kwargs(self):
        """Pass request session to form."""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Call when AnnouncementCreateForm is VALID.

        Args:
          form: The submitted AnnouncementCreateForm.

        Returns:
          The valid AnnouncementCreateForm submitted.
        """
        db = firestore.client(app=firebase_app)
        db.collection("announcements").document(form.cleaned_data["announcement_id"]).set(
            form.cleaned_data
        )
        messages.success(self.request, "Post has been saved! Do you want to create another post?")

        return super().form_valid(form)

    def form_invalid(self, form):
        """Call when AnnouncementCreateForm is INVALID.

        Args:
          form: The submitted AnnouncementCreateForm.

        Returns:
          The invalid AnnouncementCreateForm submitted.
        """
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
        context["segment"] = "announcement"
        context["title"] = "Add Announcement"
        context["hidden_fields"] = ["created", "author", "uid", "photo_url"]

        return context


class AnnouncementEditView(FormView):
    """Form view for creating announcement."""

    form_class = AnnouncementEditForm
    template_name = "announcement/create.html"
    success_url = reverse_lazy("announcement:create")

    def __init__(self):
        """Initialize AnnouncementEditView attributes."""
        self.db = firestore.client(app=firebase_app)
        self.announcement_ref = self.db.collection("announcements")

    def get_form_kwargs(self):
        """Pass announcement_id and request session to AnnouncementEditForm."""
        kwargs = super().get_form_kwargs()
        announcement_id = self.kwargs["announcement_id"]
        kwargs["request"] = self.request

        announcement = self.announcement_ref.document(announcement_id).get().to_dict()
        kwargs["announcement"] = announcement

        return kwargs

    def form_valid(self, form):
        """Call when AnnouncementCreateForm is VALID.

        Args:
          form: The submitted AnnouncementEditForm.

        Returns:
          The valid form submitted.
        """
        changed_fields = {}
        announcement_id = self.kwargs["announcement_id"]
        # TODO: default_storage.generate_filename
        if form.has_changed():
            # Accumulate all data of changed fields.
            for field in form.changed_data:
                # Delete the previous thumbnail
                if field == "thumbnail":
                    default_storage.delete(announcement_id)

                changed_fields[field] = form.cleaned_data[field]

            self.announcement_ref.document(announcement_id).update(changed_fields)

        messages.success(self.request, "Post has been edited!")

        return super().form_valid(form)

    def form_invalid(self, form):
        """Call when AnnouncementCreateForm is INVALID.

        Args:
          form: The submitted AnnouncementEditForm.

        Returns:
          The invalid form submitted.
        """
        messages.error(self.request, "Post has not been edited!")

        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to announcement edit view.

        Args:
          **kwargs: Additional keyword arguments.

        Returns:
          The dictionary data needed by announcement edit view.
        """
        context = super().get_context_data()
        context["segment"] = "announcement"
        context["title"] = "Edit Announcement"
        context["hidden_fields"] = ["created", "author", "uid", "photo_url", "updated"]

        return context


class AnnouncementDeleteView:
    """Class for deleting announcement."""

    def delete(self, announcement_id, *args, **kwargs) -> HttpResponseRedirect:
        """Delete announcement.

        Args:
          announcement_id: The unique id of the announcement.
          *args: Additional arguments.
          **kwargs: Additional Keyword arguments.

        Returns:
          HttpResponseRedirect to announcement home.
        """
        db = firestore.client(app=firebase_app)
        db.collection("announcements").document(announcement_id).delete()
        default_storage.delete(announcement_id)
        # TODO: Fix this to display success
        # messages.success(request, "successfully deleted post!")

        return HttpResponseRedirect(reverse_lazy("announcement:home"))


class AnnouncementDetailView(TemplateView):
    """Class for viewing a single announcement."""

    template_name = "announcement/view.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Get a single announcement from firestore.

        Args:
          request: The URL request.
          *args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          HttpResponse to announcement/view.html with context data.
        """
        context = self.get_context_data(**kwargs)
        db = firestore.client(app=firebase_app)

        post = (
            db.collection("announcements")
            .document(self.kwargs["announcement_id"])
            .get()
            .to_dict()
        )
        context["post"] = post

        return self.render_to_response(context)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to announcement detail view.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          The dictionary data needed by announcement detail view.
        """
        context = super().get_context_data()
        context["segment"] = "announcement"
        context["title"] = "View Announcement"

        return context

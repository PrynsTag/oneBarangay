"""Create your announcement views here."""

from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import safe
from django.template.defaultfilters import striptags
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from firebase_admin import firestore

from announcement.forms import AnnouncementCreateForm, AnnouncementEditForm
from one_barangay.mixins import ContextPageMixin, FormInvalidMixin
from one_barangay.notification import Notification
from one_barangay.settings import firebase_app


class AnnouncementHomeView(ContextPageMixin, TemplateView):
    """Template view for announcement home."""

    template_name = "announcement/home.html"
    segment = "announcement"
    title = "Announcement"
    sub_title = "View announcements / events created in oneBarangay."

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

        featured_docs = (
            db.collection("announcements")
            .where("featured", "==", True)
            .order_by("creation_date", direction="DESCENDING")
            .stream()
        )
        featured_announcements = [doc.to_dict() for doc in featured_docs]

        not_featured_docs = (
            db.collection("announcements")
            .where("featured", "==", False)
            .order_by("creation_date", direction="DESCENDING")
            .stream()
        )
        not_featured_announcements = [doc.to_dict() for doc in not_featured_docs]
        new_announcements = []
        old_announcements = []
        for post in not_featured_announcements:
            if (post["creation_date"].hour - 168) >= 0:
                old_announcements.append(post)
            else:
                new_announcements.append(post)

        context["featured_announcements"] = featured_announcements
        context["new_announcements"] = new_announcements
        context["old_announcements"] = old_announcements

        return self.render_to_response(context)


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
        form.cleaned_data["featured"] = form.cleaned_data["featured"] == "True"

        # Upload Thumbnail
        thumbnail_name = default_storage.get_valid_name(form.cleaned_data["thumbnail"].name)
        default_storage.save(thumbnail_name, form.cleaned_data["thumbnail"])

        form.cleaned_data["thumbnail_name"] = thumbnail_name
        form.cleaned_data["thumbnail"] = default_storage.url(thumbnail_name)

        db.collection("announcements").document(form.cleaned_data["announcement_id"]).set(
            form.cleaned_data, merge=True
        )
        # TODO: Go back to home after finished creating
        messages.success(self.request, "Post has been saved!")
        notification = Notification()
        notification.send_notification(
            form.cleaned_data["title"],
            safe(striptags(truncatewords(form.cleaned_data["body"], 25))),
        )

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
        context["sub_title"] = "Create announcement / events that everyone can see."
        context["hidden_fields"] = ["created", "author", "uid", "photo_url"]

        return context


# TODO: Go back to home after finished editing
#  TODO: Add buttons to prompt the user to go back
class AnnouncementEditView(FormInvalidMixin, FormView):
    """Form view for creating announcement."""

    form_class = AnnouncementEditForm
    template_name = "announcement/create.html"
    success_url = reverse_lazy("announcement:create")
    error_message = "Post has not been edited! Please fix the errors in the form."

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
        """Call when AnnouncementEditForm is VALID.

        Args:
          form: The submitted AnnouncementEditForm.

        Returns:
          The valid form submitted.
        """
        changed_fields = {}
        announcement_id = self.kwargs["announcement_id"]
        if form.has_changed():
            # Accumulate all data of changed fields.
            for field in form.changed_data:
                # Delete the previous thumbnail
                if field == "thumbnail":
                    # Delete Previous Thumbnail
                    default_storage.delete(form.cleaned_data["thumbnail_name"])

                    # Upload Thumbnail
                    thumbnail_name = default_storage.generate_filename(
                        form.cleaned_data["thumbnail"].name
                    )
                    default_storage.save(thumbnail_name, form.cleaned_data["thumbnail"])

                    form.cleaned_data["thumbnail_name"] = thumbnail_name
                    changed_fields["thumbnail_name"] = form.cleaned_data["thumbnail_name"]

                    form.cleaned_data["thumbnail"] = default_storage.url(thumbnail_name)
                if field == "featured":
                    form.cleaned_data[field] = form.cleaned_data[field] == "True"

                changed_fields[field] = form.cleaned_data[field]

            self.announcement_ref.document(announcement_id).update(changed_fields)

        messages.success(self.request, "Post has been edited!")

        return super().form_valid(form)

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
        context["sub_title"] = "Modify your existing announcement."
        context["hidden_fields"] = ["created", "author", "uid", "photo_url", "updated"]

        return context


# TODO: Notify for success or fail of deleting
# TODO: Display warning for deleting
def delete(request, announcement_id, thumbnail_name, *args, **kwargs) -> HttpResponseRedirect:
    """Delete announcement.

    Args:
      request: The URL request.
      announcement_id: The unique id of the announcement.
      thumbnail_name: The name of the thumbnail to delete.
      *args: Additional arguments.
      **kwargs: Additional Keyword arguments.

    Returns:
      HttpResponseRedirect to announcement home.
    """
    db = firestore.client(app=firebase_app)
    default_storage.delete(thumbnail_name)
    db.collection("announcements").document(announcement_id).delete()

    messages.success(request, "successfully deleted post!")

    return HttpResponseRedirect(reverse_lazy("announcement:home"))


class AnnouncementDetailView(ContextPageMixin, TemplateView):
    """Class for viewing a single announcement."""

    template_name = "announcement/view.html"
    title = "View Announcement"
    sub_title = "View each the announcement in oneBarangay in detail."
    segment = "announcement"

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

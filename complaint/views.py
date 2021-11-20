"""Create your complaint views here."""
import json
import os
from typing import Union

from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from firebase_admin import firestore
from google.api_core.exceptions import NotFound

from complaint.forms import (
    ComplaintContactForm,
    ComplaintCreateForm,
    ComplaintDetailForm,
    ComplaintDummyForm,
)
from one_barangay.local_settings import logger
from one_barangay.mixins import FormInvalidMixin
from one_barangay.notification import Notification
from one_barangay.settings import firebase_app


class ComplaintHomeView(FormView):
    """Template view for complaint home."""

    template_name = "complaint/home.html"
    form_class = ComplaintContactForm
    second_form_class = ComplaintDummyForm
    success_url = reverse_lazy("complaint:home")

    def get_context_data(self, **kwargs):
        """Get context data to complaint home view.

        Args:
          **kwargs: Additional keyword arguments.

        Returns:
          The form class needed by complaint home view.
        """
        context = super().get_context_data(**kwargs)

        if "contact_form" not in context:
            context["contact_form"] = self.form_class()
        if "dummy_form" not in context:
            context["dummy_form"] = self.second_form_class()

        context["title"] = "Complaint"
        context["sub_title"] = "A list of rows for complaints in the barangay."
        context["segment"] = "forms-complaint"
        context["id"] = "complaint_id"
        context["sort"] = [
            {"sortName": "id", "sortOrder": "asc"},
            {"sortName": "date", "sortOrder": "desc"},
        ]

        return context

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Get all complaints from firestore.

        Args:
          request: The URL request.
          *args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          Render HttpResponse to complaint/home.html along with context data.
        """
        context = self.get_context_data(**kwargs)

        db = firestore.client(app=firebase_app)
        docs = db.collection("complaints").order_by("date", direction="DESCENDING").stream()
        complaints = [doc.to_dict() for doc in docs]
        context["complaints"] = complaints

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs) -> Union[HttpResponse, HttpResponse]:
        """Post request for contact and dummy form.

        Args:
          request: The URL request.
          *args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          on success: Call form_valid with form as argument.
          on fail: Call form_invalid along with the invalid form.
        """
        # TODO: Add to appointments if date is set.
        # TODO: Add subject in form.
        if "contact_form" in request.POST:
            class_form = self.get_form_class()
            form_name = "contact_form"
        else:
            class_form = self.second_form_class  # type: ignore
            form_name = "dummy_form"

        form = self.get_form(class_form)

        if form.is_valid():
            if form_name == "contact_form":
                # TODO: Add html template.
                message = form.cleaned_data["message"]
                email = form.cleaned_data["email"]
                send_mail(
                    subject="Your complaint has been processed.",
                    message=message,
                    from_email=os.getenv("ADMIN_EMAIL"),
                    recipient_list=[email],
                )
                messages.success(request, "Complainant has been emailed successfully!")
            else:
                db = firestore.client(app=firebase_app)
                dummy_list = self.dummy_complaint(form.cleaned_data["dummy_count"])
                for dummy in dummy_list:
                    db.collection("complaints").document(dummy["complaint_id"]).set(
                        dummy, merge=True
                    )
            return self.form_valid(form=form)
        else:
            return self.form_invalid(**{form_name: form})

    def form_invalid(self, **kwargs):
        """Call when ComplaintCreateForm is INVALID.

        Args:
          **kwargs: Additional keyword arguments

        Returns:
          The invalid ComplaintContactForm or ComplaintDummyForm submitted.
        """
        if kwargs.get("contact_form"):
            form = kwargs["contact_form"]
        else:
            form = kwargs["dummy_form"]

        for field in form.errors:
            form[field].field.widget.attrs["class"] += " is-invalid"
        messages.error(
            self.request,
            "Email not sent! Please fix the errors presented in the form.",
        )
        return self.render_to_response(self.get_context_data(**kwargs))


class ComplaintCreateView(FormInvalidMixin, FormView):
    """Form view for creating complaint."""

    template_name = "complaint/create.html"
    form_class = ComplaintCreateForm
    success_url = reverse_lazy("complaint:create")
    error_message = "Complaint not sent! Please fix the " "errors displayed in the form!"

    def get_form_kwargs(self):
        """Pass request session to form."""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Call when ComplaintCreateForm is VALID.

        Args:
          form: The submitted ComplaintCreateForm.

        Returns:
          The valid ComplaintCreateForm submitted.
        """
        image = form.cleaned_data.get("image")

        if image:
            image_name = default_storage.generate_filename(image.name)
            default_storage.save(image_name, image)
            form.cleaned_data["image_url"] = default_storage.url(image_name)
            form.cleaned_data["image"] = image_name

        db = firestore.client(app=firebase_app)
        doc_ref = db.collection("complaints").document()

        form.cleaned_data["complaint_id"] = doc_ref.id
        doc_ref.set(form.cleaned_data, merge=True)
        (
            db.collection("users")
            .document(form.cleaned_data["user_id"])
            .collection("complaints")
            .document(doc_ref.id)
            .set(form.cleaned_data, merge=True)
        )

        messages.success(
            self.request,
            "The barangay has been notified! "
            "Please wait for a barangay staff "
            "to contact you on the provided information..",
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to complaint create view.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          The dictionary data needed by complaint create view.
        """
        context = super().get_context_data()
        context["title"] = "Add Complaint"
        context["sub_title"] = "A form to submit a complaint."
        context["segment"] = "forms-complaint"
        context["hidden_fields"] = ["house_num", "complaint_status", "user_id"]

        return context


class ComplaintDetailView(FormInvalidMixin, FormView):
    """Form view for viewing complaint detail."""

    template_name = "complaint/detail.html"
    form_class = ComplaintDetailForm
    success_url = reverse_lazy("complaint:home")
    error_message = "Complaint has not been saved!"

    def get_form_kwargs(self):
        """Pass complaint data to ComplaintDetailForm."""
        kwargs = super().get_form_kwargs()
        complaint_id = self.kwargs["complaint_id"]
        db = firestore.client(app=firebase_app)
        complaint = db.collection("complaints").document(complaint_id).get().to_dict()

        kwargs["complaint"] = complaint

        return kwargs

    def get(self, request, complaint_id, *args, **kwargs) -> HttpResponse:  # type: ignore
        """Get single complaint from firestore.

        Args:
          request: The URL request.
          complaint_id: The unique id of complaint.
          *args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          Render HttpResponse to complaint/home.html along with context data.
        """
        context = self.get_context_data(**kwargs)

        db = firestore.client(app=firebase_app)
        complaint = db.collection("complaints").document(complaint_id).get().to_dict()

        context["complaint"] = complaint

        return self.render_to_response(context)

    def form_valid(self, form):
        """Call when ComplaintCreateForm is VALID.

        Args:
          form: The submitted ComplaintCreateForm.

        Returns:
          The valid ComplaintCreateForm submitted.
        """
        changed_fields = {}
        if form.has_changed():
            for field in form.changed_data:
                # TODO: Remove this hack to not include field in form.changed_data.
                if field in ["date", "image_url"]:
                    continue
                else:
                    changed_fields[field] = form.cleaned_data[field]

        if changed_fields:
            if "complaint_status" in changed_fields:
                notification = Notification()
                notification.send_notification(
                    "Your complaint has been processed.",
                    f"Your complaint has changed status to {changed_fields['complaint_status']}",
                    form.cleaned_data["user_id"],
                )
            db = firestore.client(app=firebase_app)
            # Update complaints collection.
            (
                db.collection("complaints")
                .document(form.cleaned_data["complaint_id"])
                .update(changed_fields)
            )
            try:
                # Update users collection.
                (
                    db.collection("users")
                    .document(form.cleaned_data["user_id"])
                    .collection("complaints")
                    .document(form.cleaned_data["complaint_id"])
                    .update(changed_fields)
                )
            except NotFound:
                messages.info(
                    self.request,
                    "User data not updated! No user tied to this complaint.",
                )
                logger.info("[ComplaintDetailView.form_valid] User data not updated!")

            changed_fields_name = [form.fields[key].label for key in changed_fields]
            messages.success(self.request, f"Edited {''.join(changed_fields_name)} successfully!")
            logger.info(
                "[UserProfileFormView.form_valid] Form successfully updated for fields %s.",
                "".join(changed_fields_name),
            )
        else:
            messages.info(self.request, "No change detected! Database is not updated.")
            logger.info("[ComplaintDetailView.form_valid] No fields to updated!")

        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        """Get context data to complaint create view.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          The dictionary data needed by complaint create view.
        """
        context = super().get_context_data()
        context["title"] = "View Complaint"
        context["sub_title"] = "View and validate residents complaints."
        context["hidden_fields"] = ["user_id", "complaint_id"]

        return context


def delete(request) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
    """Delete complaint.

    Args:
      request: The URL Request.

    Returns:
      Redirect to complaint home.
    """
    data = json.load(request)
    complaint_data: dict = data.get("payload")
    complaint_id = complaint_data.get("complaint_id")

    db = firestore.client(app=firebase_app)

    if complaint_id:
        try:
            db.collection("complaints").document(complaint_id).delete()
            messages.success(request, "Complaint Deleted Successfully!")
        except NotFound:
            messages.error(request, "Complaint Not Found!")
        except ValueError:
            messages.error(request, "Complaint Not Found!")
    else:
        messages.error(request, "NO Complaint I.D. Provided!")

    return redirect("complaint:home")

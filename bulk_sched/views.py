"""Create your bulk_sched views here."""
import os
from datetime import datetime

import pytz
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from firebase_admin import messaging

from bulk_sched.forms import BarangayCertificate, BulkSchedCreateForm
from one_barangay.mixins import ContextPageMixin, FormInvalidMixin
from one_barangay.settings import firebase_app, firestore_db


class BulkSchedHomeView(ContextPageMixin, TemplateView):
    """Get a all the events from firestore.

    Args:
      request: The URL request.
      *args: Additional arguments.
      **kwargs: Additional keyword arguments.

    Returns:
      HttpResponse to bulk schedule home with context data.
    """

    template_name = "bulk_sched/home.html"
    title = "Bulk Scheduling"
    sub_title = "View mass events, appointments and notifications."
    segment = "bulk_sched"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Get a all the events from firestore.

        Args:
          request: The URL request.
          *args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          HttpResponse to bulk schedule home with context data.
        """
        # TODO: Convert time from utc to utc+8
        context = self.get_context_data(**kwargs)
        event_stream = firestore_db.collection("events").stream()
        events = [event.to_dict for event in event_stream]
        context["events"] = events
        context["id"] = "event_id"
        context["sort"] = ""

        return self.render_to_response(context)


class BulkSchedCreateView(FormInvalidMixin, ContextPageMixin, FormView):
    """Form view for creating bulk scheduling."""

    template_name = "bulk_sched/create.html"
    form_class = BulkSchedCreateForm
    success_url = reverse_lazy("bulk_sched:home")
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
        user_stream = firestore_db.collection("users").stream()
        title = form.cleaned_data["title"]
        body = form.cleaned_data["event_message"]
        badge = static("/assets/img/favicon/favicon.ico")

        user_data = [user.to_dict() for user in user_stream]
        emails = list(
            filter(
                lambda email: email is not None,
                [user.get("email") for user in user_data],
            )
        )
        if emails:
            send_mail(
                subject=title,
                message=body,
                from_email=os.getenv("ADMIN_EMAIL"),
                recipient_list=emails,
            )

        message_data = {
            "title": title,
            "body": body,
            "icon": badge,
            "requireInteraction": "true",
        }

        web_token = list(
            filter(
                lambda web: web is not None,
                [user.get("web_notification") for user in user_data],
            )
        )
        if web_token:
            message = messaging.MulticastMessage(
                data=message_data,
                tokens=web_token,
            )

            messaging.send_multicast(message, app=firebase_app)

        mobile_token = list(
            filter(
                lambda mobile: mobile is not None,
                [user.get("mobile_notification") for user in user_data],
            )
        )
        if mobile_token:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(title=title, body=body, image=badge),
                data=message_data,
                tokens=mobile_token,
            )
            messaging.send_multicast(message, app=firebase_app)

        event_doc = firestore_db.collection("events").document()
        event_doc.set(
            {
                "event_id": event_doc.id,
                "event_type": form.cleaned_data["event"],
                "event_purpose": form.cleaned_data["event_message"],
                "start_event": form.cleaned_data["start_date"],
                "end_event": form.cleaned_data["end_date"],
                "event_title": form.cleaned_data["title"],
                "creation_date": datetime.now(tz=pytz.timezone("Asia/Manila")),
                "notification_type": form.cleaned_data["notification_type"],
            }
        )

        messages.success(self.request, "Users Successfully Notified!")

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

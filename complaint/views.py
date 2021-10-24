"""Create your complaint views here."""
from datetime import datetime
from random import SystemRandom

import pytz
from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from faker import Faker
from firebase_admin import firestore
from google.api_core.exceptions import NotFound

from complaint.forms import ComplaintCreateForm, ComplaintDetailForm
from one_barangay.local_settings import logger
from one_barangay.settings import firebase_app


# TODO: Validators!
class ComplaintHomeView(TemplateView):
    """Template view for complaint home."""

    template_name = "complaint/home.html"

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

    def post(self, request, *args, **kwargs):
        """Save POST request to firestore complaints collection.

        Args:
          request: The URL request.
          *args: Additional arguments.
          **kwargs: Additional keyword arguments.

        Returns:
          HttpResponse with the context data.
        """
        context = self.get_context_data(**kwargs)
        dummy_list = self.dummy_complaint(int(request.POST["dummy_count"]))

        db = firestore.client(app=firebase_app)
        for dummy in dummy_list:
            db.collection("complaints").document(str(dummy["complaint_id"])).set(dummy)

        return self.render_to_response(context)

    def dummy_complaint(self, count):
        """Create dummy complaint.

        Args:
          count: The number of dummy to generate.

        Returns:
          A dictionary of single dummy complaint.
        """
        dummy_data = []
        crypto_gen = SystemRandom()
        fake = Faker(["fil_PH"])
        for _ in range(count):
            complaint_id = crypto_gen.randint(0, 999999)
            house_num = crypto_gen.randrange(100000, 999999)
            address = fake.address()
            contact_number = fake.mobile_number()
            complainant_name = fake.name()
            date = datetime.now(tz=pytz.timezone("Asia/Manila")).isoformat()
            complaint_type = crypto_gen.choice(
                [
                    "Gossip Problem",
                    "Lending Problem",
                    "Obstruction",
                    "Public Disturbance",
                ]
            )
            status = crypto_gen.choice(["Ongoing", "Handed to Police", "Resolved"])
            comment = fake.paragraphs(nb=5)[0]
            image_url = fake.image_url()

            dummy_data.append(
                {
                    "complaint_id": complaint_id,
                    "house_num": house_num,
                    "address": address,
                    "contact_number": contact_number,
                    "complainant": complainant_name,
                    "date": date,
                    "complaint_type": complaint_type,
                    "status": status,
                    "comment": comment,
                    "image_url": image_url,
                }
            )

        return dummy_data


class ComplaintCreateView(FormView):
    """Form view for creating complaint."""

    template_name = "complaint/create.html"
    form_class = ComplaintCreateForm
    success_url = reverse_lazy("complaint:create")

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
        doc_ref.set(form.cleaned_data)
        (
            db.collection("users")
            .document(form.cleaned_data["uid"])
            .collection("complaints")
            .document(doc_ref.id)
            .set(form.cleaned_data)
        )

        messages.success(
            self.request,
            "The barangay has been notified! "
            "Please wait for a barangay staff "
            "to contact you on the provided information..",
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        """Call when ComplaintCreateForm is INVALID.

        Args:
          form: The submitted ComplaintCreateForm.

        Returns:
          The invalid ComplaintCreateForm submitted.
        """
        for field in form.errors:
            form[field].field.widget.attrs["class"] += " is-invalid"

        messages.error(
            self.request, "Complaint not sent! Please fix the errors displayed in the form!"
        )

        return super().form_invalid(form)

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
        context["hidden_fields"] = ["house_num", "complaint_status", "uid"]

        return context


class ComplaintDetailView(FormView):
    """Form view for viewing complaint detail."""

    template_name = "complaint/detail.html"
    form_class = ComplaintDetailForm
    success_url = reverse_lazy("complaint:home")

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
            try:
                db = firestore.client(app=firebase_app)
                # Updated complaints collection.
                (
                    db.collection("complaints")
                    .document(form.cleaned_data["complaint_id"])
                    .update(changed_fields)
                )
                # Updated users collection.
                (
                    db.collection("users")
                    .document(form.cleaned_data["uid"])
                    .collection("complaints")
                    .document(form.cleaned_data["complaint_id"])
                    .update(changed_fields)
                )
                changed_fields_name = [form.fields[key].label for key in changed_fields]
                messages.success(
                    self.request, f"Edited {''.join(changed_fields_name)} successfully!"
                )
                logger.info(
                    "[UserProfileFormView.form_valid] Form successfully updated for fields %s.",
                    "".join(changed_fields_name),
                )

            except NotFound:
                messages.error(self.request, "Complaint has not been saved!")
                logger.info("[ComplaintDetailView.form_valid] Form NOT updated!")
        else:
            messages.info(self.request, "No change detected! Database is not updated.")
            logger.info("[ComplaintDetailView.form_valid] No fields to updated!")

        return super().form_valid(form)

    def form_invalid(self, form):
        """Call when ComplaintCreateForm is INVALID.

        Args:
          form: The submitted ComplaintCreateForm.

        Returns:
          The invalid ComplaintCreateForm submitted.
        """
        for field in form.errors:
            form[field].field.widget.attrs["class"] += " is-invalid"
        messages.error(self.request, "Complaint has not been saved!")

        return super().form_invalid(form)

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
        context["hidden_fields"] = ["uid", "complaint_id"]

        return context
